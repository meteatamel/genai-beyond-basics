RUBRIC_GENERATION_PROMPT = """
In this task, you will help me measure generate question-answer pairs to verify
an image description.

You will first identify the key words to be validated, e.g. ignoring filler or
redundant words.

You will then, for each word, generate a question-answer pair for each word. The
question should be simple and *cannot* be answered correctly based on common
sense or without reading the description. You will also tag each question as
having a type, which should be one off: object,
human, animal, food, activity, attribute, counting, color, material, spatial,
location, shape, other.

**Important**: There should be one and only one question-answer pair per key word.


Given a "description", your answer must have this format:
{
  "keywords": "Your {1}[itemized] {2}[keywords]",
  "qas": [
    The list of QAs in the format "{
      "question_id": i,
      "question": "the question",
      "answer": "the answer: yes or no",
      "choices": ["yes", "no"],
      "justification": "why is this about the keyword",
      "question_type": "the question type. One of [object, human, animal, food, activity, attribute, counting, color, material, spatial, location, shape, other]."
      }".,
  ]
}

**Important**: There should be one and only one question-answer pair per key word.
===
Some examples are below.

Description: A man posing for a selfie in a jacket and bow tie.
Answer:
{
  "keywords": "A {1}[man] {2}[posing] for a {3}[selfie] in a {4}[jacket] and a {5}[bow tie].",
  "qas": [
    {
      "question_id": 1, "question": "is there a man in the image?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There is a man in the image.", "question_type": "human"
    },
    {
      "question_id": 2, "question": "is the man posing for a selfie?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The man is posing for a selfie.", "question_type": "activity"
    },
    {
      "question_id": 3, "question": "Is the man taking a selfie?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "This is a selfie.", "question_type": "object"
    },
    {
      "question_id": 4, "question": "Is the man wearing a jacket?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The man is wearing a jacket.", "question_type": "object"
    },
    {
      "question_id": 5, "question": "Is the man wearing a bow tie?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The man is wearing a bow tie.", "question_type": "object"
    },
  ]
}

Description: A horse and several cows feed on hay.
Answer:
{
  "keywords": "A {1}[horse] and {2}[several] {3}[cows] {4}[feed] on {5}[hay]",
  "qas": [
    {
      "question_id": 1, "question": "is there a horse?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There is a horse in the image.", "question_type": "animal",
    },
    {
      "question_id": 2, "question": "are there several cows?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There are several cows in the image.", "question_type": "counting",
    },
    {
      "question_id": 3, "question": "are there cows?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There are cows in the image.", "question_type": "animal",
    },
    {
      "question_id": 4, "question": "are the horse and cows feeding on hay?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The horse and cows are feeding.", "question_type": "activity",
    },
    {
      "question_id": 5, "question": "is there hay?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There is hay in the image.", "question_type": "object",
    },
  ]
}

Description: A red colored dog.
Answer:
{
  "keywords": "A {1}[red colored] {2}[dog].",
  "qas": [
    {
      "question_id": 1, "question": "is the dog red?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There is a red colored dog in the image.", "question_type": "color",
    },
    {
      "question_id": 2, "question": "is there a dog?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There is a dog in the image.", "question_type": "animal",
    },
  ]
}

Description: A busy intersection with an ice cream truck driving by.
Answer:
{
  "keywords": "A {1}[busy] {2}[intersection] with an {3}[ice cream truck] {4}[driving by].",
  "qas": [
    {
      "question_id": 1, "question": "is this a busy intersection?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The intersection is busy.", "question_type": "attribute",
    },
    {
      "question_id": 2, "question": "is this an intersection?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There is a busy intersection.", "question_type": "object",
    },
    {
      "question_id": 3, "question": "is there an ice cream truck?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There is an ice cream truck.", "question_type": "object",
    },
    {
      "question_id": 4, "question": "is the ice cream truck driving by?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The ice cream truck is driving by.", "question_type": "activity",
    },
  ]
}

Description: Portrait of a gecko wearing a train conductor's hat and holding a flag that has a yin-yang symbol on it. Woodcut.
Answer:
{
  "keywords": "{1}[Portrait] of a {2}[gecko] {3}[wearing] a {4}[train conductor's hat] and {5}[holding] a {6}[flag] that has a {7}[yin-yang symbol] on it. {8}[Woodcut].",
  "qas": [
    {
      "question_id": 1, "question": "is this a portrait?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "This is a portrait.", "question_type": "attribute",
    },
    {
      "question_id": 2, "question": "is there a gecko?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There is a gecko.", "question_type": "animal",
    },
    {
      "question_id": 3, "question": "is the gecko wearing a hat?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The gecko is wearing a train conductor's hat.", "question_type": "activity",
    },
    {
      "question_id": 4, "question": "is the gecko wearing a train conductor's hat?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The gecko is wearing a train conductor's hat.", "question_type": "attribute",
    },
    {
      "question_id": 5, "question": "is the gecko holding a flag", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The gecko is holding a flag.", "question_type": "activity",
    },
    {
      "question_id": 6, "question": "is there a flag?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There is a flag.", "question_type": "object",
    },
    {
      "question_id": 7, "question": "does the flag have a yin-yang symbol?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The flag has a yin-yang symbol on it.", "question_type": "attribute",
    },
    {
      "question_id": 8, "question": "is this a woodcut?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "woodcut.", "question_type": "attribute",
    },
  ]
}

Description: A woman is showing a watermelon slice to a woman on a scooter.
Answer:
{
  "keywords": "A {1}[woman] is {2}[showing] a {3}[watermelon slice] to a {4}[woman] {5}[on] a {6}[scooter].",
  "qas": [
    {
      "question_id": 1, "question": "is there a woman?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "This is a woman.", "question_type": "human",
    },
    {
      "question_id": 2, "question": "is one woman showing a watermelon slice to another woman?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "A woman is showing a watermelon slice to a woman.", "question_type": "activity",
    },
    {
      "question_id": 3, "question": "is there a watermelon slice?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The watermelon slice is a watermelon slice.", "question_type": "food",
    },
    {
      "question_id": 4, "question": "are there two women?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "A woman is showing a watermelon slice to a woman.", "question_type": "human",
    },
    {
      "question_id": 5, "question": "is one of the women on a scooter?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "A woman is on a scooter.", "question_type": "spatial",
    },
    {
      "question_id": 6, "question": "is there a scooter?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There is a scooter.", "question_type": "object",
    },
  ]
}

Description: A photo of three dogs.
Answer:
{
  "keywords": "A {1}[photo] of {2}[three] {3}[dogs].",
  "qas": [
    {
      "question_id": 1, "question": "is this a photo?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "This is a photo of three dogs.", "question_type": "attribute",
    },
    {
      "question_id": 2, "question": "are there three dogs?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "three dogs.", "question_type": "counting",
    },
    {
      "question_id": 3, "question": "is there a dog?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There is a dog.", "question_type": "object",
    },
  ]
}

Description: A white milk truck with a license plate that reads 'pro milk'.
Answer:
{
  "keywords": "A {1}[white] {2}[milk truck] with a {3}[license plate] that reads {4}['pro milk'].",
  "qas": [
    {
      "question_id": 1, "question": "is this a white truck?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "This is a white milk truck.", "question_type": "attribute",
    },
    {
      "question_id": 2, "question": "is there a milk truck?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "This is a white milk truck.", "question_type": "object",
    },
    {
      "question_id": 3, "question": "is there a license plate on the vehicle?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "A white milk truck with a license plate.", "question_type": "object",
    },
    {
      "question_id": 4, "question": "does the license plate read 'pro milk'?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The license plate reads 'pro milk'.", "question_type": "attribute",
    },
  ]
}

Description: A person sitting on a horse in air over gate in grass with people and trees in background.
Answer:
{
  "keywords": "A {1}[person] {2}[sitting] {3}[on] a {4}[horse] {5}[in air] {6}[over] {7}[gate] in {8}[grass] with {9}[people] and {10}[trees] in {11}[background].",
  "qas": [
    {
      "question_id": 1, "question": "is there a person?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "This is a person.", "question_type": "human",
    },
    {
      "question_id": 2, "question": "is the person sitting?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "A person is sitting on a horse.", "question_type": "activity",
    },
    {
      "question_id": 3, "question": "is the person on a horse?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "A person is sitting on a horse.", "question_type": "spatial",
    },
    {
      "question_id": 4, "question": "is there a horse?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "A person is sitting on a horse.", "question_type": "object",
    },
    {
      "question_id": 5, "question": "is the horse in the air?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The horse is in the air.", "question_type": "attribute",
    },
    {
      "question_id": 6, "question": "is the horse over the gate?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The horse is over the gate.", "question_type": "spatial",
    },
    {
      "question_id": 7, "question": "is there a gate?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The horse is over the gate.", "question_type": "object",
    },
    {
      "question_id": 8, "question": "is there grass?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "The horse is in the grass.", "question_type": "object",
    },
    {
      "question_id": 9, "question": "are there people?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There are people.", "question_type": "human",
    },
    {
      "question_id": 10, "question": "are there trees?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There are trees.", "question_type": "object",
    },
    {
      "question_id": 11, "question": "are there people and trees in the background?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There people and trees in the background.", "question_type": "human",
    },
  ]
}

Description: a red blue and yellow train and some people on a platform
Answer:
{
  "keywords": "a {1}[red blue and yellow] {2}[train] and {3}[some] {4}[people] on a {5}[platform]",
  "qas": [
    {
      "question_id": 1, "question": "is the train red blue and yellow?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "This is a red blue and yellow train.", "question_type": "color",
    },
    {
      "question_id": 2, "question": "is there a train?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There is a train.", "question_type": "object",
    },
    {
      "question_id": 3, "question": "Are there some people?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There are some people.", "question_type": "counting",
    },
    {
      "question_id": 4, "question": "are the people on the platform?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There are some people on the platform.", "question_type": "human",
    },
    {
      "question_id": 5, "question": "is there a platform?", "answer": "yes", "choices": ["yes", "no"],
      "justification": "There is a platform.", "question_type": "object",
    },
  ]
}

Description:
{prompt}
Answer:
"""

RUBRIC_VALIDATOR_PROMPT = """
# Instructions
Look at the image carefully and answer each question with a yes or no:
{rubrics}

# Image
{image}

# Output Format
<question>
Question: repeat the original question
Verdict: yes|no
</question>
"""


