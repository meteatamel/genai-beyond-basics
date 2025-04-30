import pandas
import sys
from vertexai.evaluation import (
    EvalTask,
    MetricPromptTemplateExamples
)
from vertexai.generative_models import GenerativeModel

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import get_experiment_name, print_eval_result

# Pointwise (single model) metrics can be used in 2 ways:
# 1- Bring-your-own-response (BYOR) mode where the model responses are provided rather than calling the model.
# 2- Bring a model and use that model to get responses from.
# See: https://cloud.google.com/vertex-ai/generative-ai/docs/models/metrics-templates#overview

# Using Extreme Summarization (XSum) Dataset:
# https://huggingface.co/datasets/EdinburghNLP/xsum/viewer?row=3&views%5B%5D=train
prompt = "Summarize the following article: "

context = [
    'The full cost of damage in Newton Stewart, one of the areas worst affected, is still being assessed. Repair work is ongoing in Hawick and many roads in Peeblesshire remain badly affected by standing water. Trains on the west coast mainline face disruption due to damage at the Lamington Viaduct. Many businesses and householders were affected by flooding in Newton Stewart after the River Cree overflowed into the town. First Minister Nicola Sturgeon visited the area to inspect the damage. The waters breached a retaining wall, flooding many commercial properties on Victoria Street - the main shopping thoroughfare. Jeanette Tate, who owns the Cinnamon Cafe which was badly affected, said she could not fault the multi-agency response once the flood hit. However, she said more preventative work could have been carried out to ensure the retaining wall did not fail. "It is difficult but I do think there is so much publicity for Dumfries and the Nith - and I totally appreciate that - but it is almost like we\'re neglected or forgotten," she said. "That may not be true but it is perhaps my perspective over the last few days. "Why were you not ready to help us a bit more when the warning and the alarm alerts had gone out?" Meanwhile, a flood alert remains in place across the Borders because of the constant rain. Peebles was badly hit by problems, sparking calls to introduce more defences in the area. Scottish Borders Council has put a list on its website of the roads worst affected and drivers have been urged not to ignore closure signs. The Labour Party\'s deputy Scottish leader Alex Rowley was in Hawick on Monday to see the situation first hand. He said it was important to get the flood protection plan right but backed calls to speed up the process. "I was quite taken aback by the amount of damage that has been done," he said. "Obviously it is heart-breaking for people who have been forced out of their homes and the impact on businesses." He said it was important that "immediate steps" were taken to protect the areas most vulnerable and a clear timetable put in place for flood prevention plans. Have you been affected by flooding in Dumfries and Galloway or the Borders? Tell us about your experience of the situation and how it was handled. Email us on selkirk.news@bbc.co.uk or dumfries@bbc.co.uk.',
    'A fire alarm went off at the Holiday Inn in Hope Street at about 04:20 BST on Saturday and guests were asked to leave the hotel. As they gathered outside they saw the two buses, parked side-by-side in the car park, engulfed by flames. One of the tour groups is from Germany, the other from China and Taiwan. It was their first night in Northern Ireland. The driver of one of the buses said many of the passengers had left personal belongings on board and these had been destroyed. Both groups have organised replacement coaches and will begin their tour of the north coast later than they had planned. Police have appealed for information about the attack. Insp David Gibson said: "It appears as though the fire started under one of the buses before spreading to the second. "While the exact cause is still under investigation, it is thought that the fire was started deliberately.',
    'Ferrari appeared in a position to challenge until the final laps, when the Mercedes stretched their legs to go half a second clear of the red cars. Sebastian Vettel will start third ahead of team-mate Kimi Raikkonen. The world champion subsequently escaped punishment for reversing in the pit lane, which could have seen him stripped of pole. But stewards only handed Hamilton a reprimand, after governing body the FIA said "no clear instruction was given on where he should park". Belgian Stoffel Vandoorne out-qualified McLaren team-mate Jenson Button on his Formula 1 debut. Vandoorne was 12th and Button 14th, complaining of a handling imbalance on his final lap but admitting the newcomer "did a good job and I didn\'t". Mercedes were wary of Ferrari\'s pace before qualifying after Vettel and Raikkonen finished one-two in final practice, and their concerns appeared to be well founded as the red cars mixed it with the silver through most of qualifying. After the first runs, Rosberg was ahead, with Vettel and Raikkonen splitting him from Hamilton, who made a mistake at the final corner on his first lap. But Hamilton saved his best for last, fastest in every sector of his final attempt, to beat Rosberg by just 0.077secs after the German had out-paced him throughout practice and in the first qualifying session. Vettel rued a mistake at the final corner on his last lap, but the truth is that with the gap at 0.517secs to Hamilton there was nothing he could have done. The gap suggests Mercedes are favourites for the race, even if Ferrari can be expected to push them. Vettel said: "Last year we were very strong in the race and I think we are in good shape for tomorrow. We will try to give them a hard time." Vandoorne\'s preparations for his grand prix debut were far from ideal - he only found out he was racing on Thursday when FIA doctors declared Fernando Alonso unfit because of a broken rib sustained in his huge crash at the first race of the season in Australia two weeks ago. The Belgian rookie had to fly overnight from Japan, where he had been testing in the Super Formula car he races there, and arrived in Bahrain only hours before first practice on Friday. He also had a difficult final practice, missing all but the final quarter of the session because of a water leak. Button was quicker in the first qualifying session, but Vandoorne pipped him by 0.064secs when it mattered. The 24-year-old said: "I knew after yesterday I had quite similar pace to Jenson and I knew if I improved a little bit I could maybe challenge him and even out-qualify him and that is what has happened. "Jenson is a very good benchmark for me because he is a world champion and he is well known to the team so I am very satisfied with the qualifying." Button, who was 0.5secs quicker than Vandoorne in the first session, complained of oversteer on his final run in the second: "Q1 was what I was expecting. Q2 he did a good job and I didn\'t. Very, very good job. We knew how quick he was." The controversial new elimination qualifying system was retained for this race despite teams voting at the first race in Australia to go back to the 2015 system. FIA president Jean Todt said earlier on Saturday that he "felt it necessary to give new qualifying one more chance", adding: "We live in a world where there is too much over reaction." The system worked on the basis of mixing up the grid a little - Force India\'s Sergio Perez ended up out of position in 18th place after the team miscalculated the timing of his final run, leaving him not enough time to complete it before the elimination clock timed him out. But it will come in for more criticism as a result of lack of track action at the end of each session. There were three minutes at the end of the first session with no cars on the circuit, and the end of the second session was a similar damp squib. Only one car - Nico Hulkenberg\'s Force India - was out on the track with six minutes to go. The two Williams cars did go out in the final three minutes but were already through to Q3 and so nothing was at stake. The teams are meeting with Todt and F1 commercial boss Bernie Ecclestone on Sunday at noon local time to decide on what to do with qualifying for the rest of the season. Todt said he was "optimistic" they would be able to reach unanimous agreement on a change. "We should listen to the people watching on TV," Rosberg said. "If they are still unhappy, which I am sure they will be, we should change it." Red Bull\'s Daniel Ricciardo was fifth on the grid, ahead of the Williams cars of Valtteri Bottas and Felipe Massa and Force India\'s Nico Hulkenberg. Ricciardo\'s team-mate Daniil Kvyat was eliminated during the second session - way below the team\'s expectation - and the Renault of Brit Jolyon Palmer only managed 19th fastest. German Mercedes protege Pascal Wehrlein managed an excellent 16th in the Manor car. Bahrain GP qualifying results Bahrain GP coverage details',
    'Gundogan, 26, told BBC Sport he "can see the finishing line" after tearing cruciate knee ligaments in December, but will not rush his return. The German missed the 2014 World Cup following back surgery that kept him out for a year, and sat out Euro 2016 because of a dislocated kneecap. He said: "It is heavy mentally to accept that." Gundogan will not be fit for the start of the Premier League season at Brighton on 12 August but said his recovery time is now being measured in "weeks" rather than months. He told BBC Sport: "It is really hard always to fall and fight your way back. You feel good and feel ready, then you get the next kick. "The worst part is behind me now. I want to feel ready when I am fully back. I want to feel safe and confident. I don\'t mind if it is two weeks or six." Gundogan made 15 appearances and scored five goals in his debut season for City following his £20m move from Borussia Dortmund. He is eager to get on the field again and was impressed at the club\'s 4-1 win over Real Madrid in a pre-season game in Los Angeles on Wednesday. Manager Pep Guardiola has made five new signings already this summer and continues to have an interest in Arsenal forward Alexis Sanchez and Monaco\'s Kylian Mbappe. Gundogan said: "Optimism for the season is big. It is huge, definitely. "We felt that last year as well but it was a completely new experience for all of us. We know the Premier League a bit more now and can\'t wait for the season to start." City complete their three-match tour of the United States against Tottenham in Nashville on Saturday. Chelsea manager Antonio Conte said earlier this week he did not feel Tottenham were judged by the same standards as his own side, City and Manchester United. Spurs have had the advantage in their recent meetings with City, winning three and drawing one of their last four Premier League games. And Gundogan thinks they are a major threat. He said: "Tottenham are a great team. They have the style of football. They have young English players. Our experience last season shows it is really tough to beat them. "They are really uncomfortable to play against. "I am pretty sure, even if they will not say it loud, the people who know the Premier League know Tottenham are definitely a competitor for the title.',
]

prompts = [prompt + item for item in context]

eval_dataset = pandas.DataFrame(
    {
        "prompt": prompts,
        # history is needed for multi-turn metrics
        # "history": history
    }
)

metrics = [
    # Metrics that need 'prompt' and 'response' columns
    MetricPromptTemplateExamples.Pointwise.FLUENCY,
    # MetricPromptTemplateExamples.Pointwise.COHERENCE,
    # MetricPromptTemplateExamples.Pointwise.GROUNDEDNESS,
    # MetricPromptTemplateExamples.Pointwise.SAFETY,
    # MetricPromptTemplateExamples.Pointwise.INSTRUCTION_FOLLOWING,
    # MetricPromptTemplateExamples.Pointwise.VERBOSITY,
    # MetricPromptTemplateExamples.Pointwise.TEXT_QUALITY,
    # MetricPromptTemplateExamples.Pointwise.SUMMARIZATION_QUALITY,
    # MetricPromptTemplateExamples.Pointwise.QUESTION_ANSWERING_QUALITY,

    # Metrics that additionally need 'history' column
    # MetricPromptTemplateExamples.Pointwise.MULTI_TURN_CHAT_QUALITY,
    # MetricPromptTemplateExamples.Pointwise.MULTI_TURN_SAFETY_QUALITY
]

# Pointwise metrics with bring-your-own-response (BYOR) mode where the model
# responses are provided rather than calling the model.
# https://cloud.google.com/vertex-ai/generative-ai/docs/models/metrics-templates#overview
def byor():

    # Responses a provided rather than calling the model.
    responses = [
        "Clean-up operations are continuing across the Scottish Borders and Dumfries and Galloway after flooding caused by Storm Frank.",
        "Two tourist buses have been destroyed by fire in a suspected arson attack in Belfast city centre.",
        "Lewis Hamilton stormed to pole position at the Bahrain Grand Prix ahead of Mercedes team-mate Nico Rosberg.",
        "Manchester City midfielder Ilkay Gundogan says it has been mentally tough to overcome a third major injury.",
    ]
    eval_dataset["response"] = responses

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=metrics,
        experiment=get_experiment_name(__file__, "byor")
    )

    eval_result = eval_task.evaluate()
    print_eval_result(eval_result, colwidth=50)


# Pointwise metrics with a provided model to get responses from.
# https://cloud.google.com/vertex-ai/generative-ai/docs/models/metrics-templates#overview
def model():

    # Model to get responses from
    model=GenerativeModel("gemini-2.0-flash")

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=metrics,
        experiment=get_experiment_name(__file__, "model")
    )

    eval_result = eval_task.evaluate(
        model=model
    )
    print_eval_result(eval_result, colwidth=50)


if __name__ == "__main__":
    globals()[sys.argv[1]]()
