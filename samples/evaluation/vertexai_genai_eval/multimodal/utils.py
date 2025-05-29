from collections.abc import Sequence
from dataclasses import dataclass, field
import json
import numpy as np
import re
from typing import Any

_QUESTION_REGEX = re.compile(r"Question:(.*?)Verdict:", re.DOTALL)
_VERDICT_REGEX = re.compile("Verdict:(.*)")
_QUESTION_BLOCK_REGEX = re.compile("<question>(.*?)</question>", re.DOTALL)


@dataclass(kw_only=True) #, frozen=True)
class QARecord:
    """A basic QA Record for storing question-answer pairs.

    Attributes:
        question: Question text.
        question_type: Category of question.
        gt_answer: Ground-truth answer to the question.
        answer_choices: Possible answers for multiple choice questions.
        justification: How the question relates to the prompt.
    """

    question: str = ""
    question_type: str = ""
    gt_answer: str = ""
    answer_choices: Sequence[str] = field(default_factory=list)
    justification: str = ""


class QAResult(QARecord):
    """A basic QA Result for storing question-answer results.

    Attributes:
        result: The result of answering the question.
    """

    result: str = ""

    def __init__(self, qa_record: QARecord, result: str):
        super().__init__(
            question=qa_record.question,
            question_type=qa_record.question_type,
            gt_answer=qa_record.gt_answer,
            answer_choices=qa_record.answer_choices,
            justification=qa_record.justification,
        )
        self.result = result


def parse_json_to_qa_records(json_response: str, parse_for_image=True) -> dict[str, Any]:
    """
    Parse the JSON response and convert it to a questions and QARecords.

    Args:
        json_response: JSON string containing the QA data.

    Returns:
        Dict with keywords, questions, and QARecord objects.

    Raises:
        json.JSONDecodeError: If JSON parsing fails
        KeyError: If expected keys are missing from the JSON structure
    """
    json_response = re.sub(
        r"(.*```json|```.*)",
        "",
        json_response.strip(),
    )
    try:
        # Parse JSON string to Python object
        data = json.loads(json_response)
        qa_records = []

        # Process each QA pair in the QAs array
        rubrics = []
        for qa in data["qas"]:
            record = QARecord(
                question=qa["question"],
                #question_type=qa["question_type"],
                question_type=qa["question_type"] if parse_for_image else "",
                gt_answer=qa["answer"],
                answer_choices=qa["choices"],
                justification=qa["justification"],
            )
            qa_records.append(record)
            rubrics.append(
                f"<question>{record.question}<choices>{','.join(record.answer_choices)}"
            )
        return {
            "questions": "\n".join(rubrics),
            "keywords": data["keywords"],
            "qa_records": qa_records,
        }
    except json.JSONDecodeError as e:
        return {
            "questions": f"Error decoding JSON response: {str(e)}",
            "keywords": "",
            "qa_records": json_response,
        }
    except KeyError as e:
        return {
            "questions": f"Missing required key in JSON structure: {str(e)}",
            "keywords": "",
            "qa_records": json_response,
        }


def parse_rubric_results(results: list[str]) -> dict[str, Any]:
    """Parses the rubric results from the rubric validator response."""
    rubric_results = {}
    for result in results:
        rubric_verdicts = _parse_question_blocks(result)
        for rubric, verdict in rubric_verdicts:
            rubric_results[rubric.lower()] = verdict.lower()
    return {"rubric_results": rubric_results}


def _parse_question_blocks(txt: str) -> list[tuple[str, bool]]:
    """Parses the question blocks from the rubric validator response."""
    responses = []
    question_blocks = _QUESTION_BLOCK_REGEX.findall(txt)
    if not question_blocks:
        question_blocks = [txt]
    for block in question_blocks:
        q = _parse_question(block)
        v = _parse_verdict(block)
        if q is not None and v is not None:
            responses.append((q, v))
    return responses


def _parse_question(txt: str):
    """Parses the question from the rubric validator response."""
    if not isinstance(txt, str) or not txt:
        return None
    try:
        txt = txt.split("Verdict:")[0]
        if "Question:" in txt:
            return txt.split("Question:")[-1].strip()
        if question := _QUESTION_REGEX.findall(txt):
            return question[0].strip()
    except Exception as e:
        print(f"Failed to parse question: {str(e)}")
        return None


def _parse_verdict(txt: str):
    """Parses the verdict from the rubric validator response."""
    if not isinstance(txt, str) or not txt:
        return None
    try:
        if verdict := _VERDICT_REGEX.findall(txt):
            verdict = verdict[0].strip()
            return verdict
    except Exception as e:
        print(f"Failed to parse question: {str(e)}")
        return None

def compute_scores(df: "pd.DataFrame") -> "pd.DataFrame":
    """Computes scores for each row based on QA results."""
    qa_results = []
    final_scores = []
    for idx, row in df.iterrows():
        rubric_results = {}
        for key in row.keys():
            if "rubric_results" in key:
                rubric_results = row[key]
        scores = []
        results = []
        for qa in row["qa_records"]:
            q = qa.question.lower()
            if q in rubric_results:
                if qa.gt_answer.lower() in rubric_results[q]:
                    results.append(QAResult(qa, f"{qa.gt_answer} ✓"))
                    scores.append(1)
                else:
                    results.append(QAResult(qa, f"{rubric_results[q]} 🗴"))
                    scores.append(0)
            else:
                results.append(QAResult(qa, "no result"))
                scores.append(0)
        qa_results.append(results)
        final_scores.append(np.mean(scores))
    df_with_score = df.assign(qa_results=qa_results, final_score=final_scores)
    return df_with_score