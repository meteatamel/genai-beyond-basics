RUBRIC_GENERATION_PROMPT = """Given a video description and the groundable words
in it, generate multiple-choice questions that verify if the video description
is correct.

The goal is to ask questions about entities, objects, attributes, actions, colors,
spatial relations, temporal relations, styles and scenes, when these are present
in the description.

Make sure that all options are substantially different from each other and only
one option can be the correct one based on the description. Do not include other
parts of the description as a non correct option.

Justify why the other options cannot be true based on the description and
question. Also, make sure that the question cannot be answered correctly only
based on common sense and without reading the description.

Each generated question should be independent of the other ones and it should be
able to be understood without knowing the other questions; avoid referring to
entities/objects/places from previous questions.

Finally, avoid asking very general questions, such as 'What is in the video?',
or 'Name a character in the video'.

Generate the multiple-choice questions in the exact same format as the examples
that follow. Do not add asterisks, white spaces, or any other reformatting and
explanation that deviate from the formatting of the following examples.

**Important**: There should be one and only one question-answer pair per key word.
**Important**: answer value MUST BE only one of the following letters a, b, c, or d. And it MUST BE ALWAYS in lowercase!


Given a "description", your answer must respond using this format:
{
  "keywords": "Your {1}[itemized] {2}[keywords]",
  "qas": [
    The list of QAs in the format "{
      "question_id": i,
      "question": "the question",
      "choices": ["a) option 1", "b) option 2", "c) option 3", "d) option 4"],
      "justification": "why is this about the keyword",
      "answer": "the identifier of the right answer (i.e. a, b, c, or d)",
      }",
  ]
}

===
Some examples are below.

Description:

Close up of grapes on a rotating table.
Answer:
{
  "keywords": "{1}[Close up, style, 1.0] of {2}[grapes, object, 1.0] {3}[on a {4}[rotating, action, 1.0] {5}[table, spatial relation, 1.0]",
  "qas": [
    {
      "question_id": 1, "question": " How is the object displayed in the video shot in the camera?", "choices": ["a) long shot", "b) close up", "c) glimpse", "d) slow motion"],
      "justification": "The grapes, which is the main object displayed in the video ({2}) is presented with a close up ({1}). Given this, none of the other options can be correct as they are the opposite or contradict the description."
      "answer": "b"
    },
    {
      "question_id": 2, "question": "What is the object that the camera focuses on during the video?", "choices": ["a) table", "b) pears", "c) blackberries", "d) grapes"],
       "justification": "the close up is happening on the grapes ({2}). A table is also present in the video ({5}) but it is not the main focus (close up) of the video. Pears and blackberries are not present in the video.",
      "answer": "d"
    },
    {
      "question_id": 3, "question": "Where are the grapes placed in the video?", "choices": ["a) table", "b) chair", "c) bowl", "d) plate'],
      "justification": "the grapes are placed on a table ({3}). Chair is not correct, but it is similar furniture to table and could be found next to it, and bowl and plate are reasonable answers for placing grapes but not true here based on the description.",
      "answer": "a",

    },
    {
      "question_id": 4, "question": "What movement does the table in the video follows?", "choices": ["a) it stays still", "b) it is moved to the right", "c) it is moved to the left", "d) it rotates"],
      "justification": "the table is rotating ({4}, {5}). Staying still is typically how a table is depicted in videos, and moving it right or left are other movements that we often see but they are not true according to the description.",
      "answer": d,
    }
  ]
}

Description:

Turtle swimming in ocean.

Answer:

{
  "keywords": "{1}[Turtle, entity, 1.0] {2}[swimming, action, 1.0] {3}[in ocean, spatial relation, 1.0]",
  "qas": [
    {
      "question_id": 1,
      "question": "What animal is present in the video?",
      "choices": ["a) fish", "b) dolphin", "c) turtle", "d) whale"],
      "justification": "turtle is the correct answer ({1}). All of fish, dolphin and whale are animals that live and swim in the ocean, so they are reasonable responses to such a question, but not the correct ones according to the description.",
      "answer": "c"
    },
    {
      "question_id": 2,
      "question": "What is the turtle doing in the video?",
      "choices": ["a) swims", "b) walks", "c) stays still", "d) moves the legs statically"],
      "justification": "the turtle is swimming ({2}). Staying still, walking or moving the legs without walking are typical movements that a turtle does, but they are not true according to the description.",
      "answer": "a"
    },
    {
      "question_id": 3,
      "question": "Where is the video taking place?",
      "choices": ["a) in the beach", "b) in the ocean", "c) in a boat", "d) in a lake"],
      "justification": "the turtle is swimming in the ocean ({3}). All other options are not true, but they would look similar to an ocean and they are of similar topic.",
      "answer": "b"
    }
  ]
}

Description:

A fat rabbit wearing a purple robe walking through a fantasy landscape.

Answer:

{
  "keywords": "A {1}[fat, attribute, 1.0] {2}[rabbit, entity, 1.0] {3}[wearing a {4}[purple, color, 1.0] robe, attribute, 1.0] {5}[walking, action, 1.0] through a {6}[fantasy landscape, scene, 1.0]",
  "qas": [
    {
      "question_id": 1,
      "question": "What is the most appropriate description for the animal of the video?",
      "choices": ["a) thin", "b) regular", "c) slim", "d) fat"],
      "justification": "the rabbit in the video is fat ({1}). The options thin and slim are opposite of the attribute mentioned in the description and the regular adjective checks whether it is obvious that the rabbit has a weight above normal.",
      "answer": "d"
    },
    {
      "question_id": 2,
      "question": "Who wears a robe in the video?",
      "choices": ["a) rabbit", "b) hare", "c) squirrel", "d) rat"],
      "justification": "the rabbit is the animal that wears a robe in the video ({2}). Hare is an animal very similar to rabbit, and the other two options (squirrel and rat) are also similar but not true according to the description.",
      "answer": "a"
    },
    {
      "question_id": 3,
      "question": "What is the rabbit wearing in the video?",
      "choices": ["a) nothing", "b) dress", "c) robe", "d) jumpsuit"],
      "justification": "the rabbit is wearing a robe ({3}). Nothing is what normally an animal is wearing, and the options dress and jumpsuit are similar to the robe but not true according to the description.",
      "answer": "c"
    },
    {
      "question_id": 4,
      "question": "What is the color of the clothing that the rabbit wears in the video?",
      "choices": ["a) purple", "b) blue", "c) pink", "d) green"],
      "justification": "the rabbit is wearing a purple robe ({4}). the options blue, pink and green are colors similar to purple.",
      "answer": "a"
    },
    {
      "question_id": 5,
      "question": "What is the rabbit doing in the video?",
      "choices": ["a) running", "b) walking", "c) standing", "d) jumping"],
      "justification": "the rabbit is walking through a fantasy landscape ({5}, {6}). The options running and standing are similar to walking, and jumping is an action that could be performed by a rabbit, but not true according to the description.",
      "answer": "b"
    },
    {
      "question_id": 6,
      "question": "Where is the video taking place?",
      "choices": ["a) fields", "b) countryside", "c) fantasy landscape", "d) mountains"],
      "justification": "the rabbit is walking through a fantasy landscape ({6}). The options fields, countryside, and mountains are different types of landscapes, but they are real-world scenes instead of fantasy ones.",
      "answer": "c"
    }
  ]
}

Description:

A beautiful coastal beach in spring, waves lapping on sand by Hokusai, in the style of Ukiyo

Answer:

{
  "keywords": "A {1}[beautiful coastal beach, scene, 1.0] {2}[in spring, temporal relation, 1.0], {3}[waves, scene, 1.0] {4}[lapping, action, 1.0] {5}[on sand, spatial relation, 1.0] {6}[by Hokusai, style, 1.0], {7}[in the style of Ukiyo, style, 1.0]",
  "qas": [
    {
      "question_id": 1,
      "question": "Where is the video taking place?",
      "choices": ["a) cliffs", "b) harbor", "c) coastal park", "d) coastal beach"],
      "justification": "the main scene is a beautiful coastal beach ({1}). The options cliffs, harbor, and coastal park are similar to coastal beach but not true according to the description.",
      "answer": "d"
    },
    {
      "question_id": 2,
      "question": "Which season is most likely during the video?",
      "choices": ["a) spring", "b) summer", "c) autumn", "d) winter"],
      "justification": "the video shows a coastal beach in spring ({2}). The options summer, autumn and winter are other seasons that are not true according to the description.",
      "answer": "a"
    },
    {
      "question_id": 3,
      "question": "What is the level of movement of the sea during the video?",
      "choices": ["a) calm", "b) wavy", "c) slightly moving", "d) ripply"],
      "justification": "the sea is wavy ({3}). The options calm, slightly moving, and ripply are different levels of movement of the sea and they are all different enough from wavy.",
      "answer": "b"
    },
    {
      "question_id": 4,
      "question": "What is the movement of the sea during the video?",
      "choices": ["a) gentle waves are coming to the shore", "b) there is a tide", "c) waves are lapping on the shore", "d) there are sea ripples"],
      "justification": "the sea is lapping on the shore ({4}). The other provided options are either of less intensity (gentle waves are coming to the shore, there are sea ripples) or the exact opposite (there is a tide).",
      "answer": "c"
    },
    {
      "question_id": 5,
      "question": "Where does the sea move to during the video?",
      "choices": ["a) sand", "b) rocks", "c) cliffs", "d) pebbles"],
      "justification": "the waves are lapping on sand ({5}). The options pebbles, rocks, and cliffs are different types of ground typically by the sea and have different levels of solidity.",
      "answer": "a"
    },
    {
      "question_id": 6,
      "question": "Whose artist is the theme of the scene similar to?",
      "choices": ["a) Utamaro", "b) Hokusai", "c) Hiroshige", "d) Yoshitoshi"],
      "justification": "the theme of the scene resembles a painting of Hokusai. The other options are other Japanese artists that are similar to Hokusai.",
      "answer": "b"
    },
    {
      "question_id": 7,
      "question": "Which Japanese painting style is most similar to the video?",
      "choices": ["a) Ukiyo", "b) Nihonga", "c) Sumi", "d) ink calligraphy"],
      "justification": "the video scene is in the style of Ukiyo ({7}). The other options are other types of Japanese painting styles that are not similar to the video according to the description.",
      "answer": "a"
    }
  ]
}

Description:

Mysterious scene of Sherlock Holmes investigating a crime scene at 221B Baker Street, forced perspective

Answer:

{
  "keywords": "{1}[Mysterious scene, style, 1.0] of {2}[Sherlock Holmes, entity, 1.0] {3}[investigating, action, 1.0] a {4}[crime scene, scene, 1.0] {5}[at 221B Baker Street, spatial relation, 1.0], {6}[forced perspective, style, 1.0]",
  "qas": [
    {
      "question_id": 1,
      "question": "What is the vibe of the video?",
      "choices": ["a) light", "b) mysterious", "c) scary", "d) calm"],
      "justification": "the vibe of the video is mysterious ({1}). The options light and calm are opposite vibes to mysterious, and scary is similar to mysterious but more exaggerated and not true according to the description.",
      "answer": "b"
    },
    {
      "question_id": 2,
      "question": "What is the name of the person investigating the scene in the video?",
      "choices": ["a) Sherlock Holmes", "b) Watson", "c) John Luther", "d) Hercule Poirot"],
      "justification": "the video shows Sherlock Holmes in the scene ({2}). Watson is another character from the Sherlock Holmes show but not the correct one according to the description, and John Luther and Hercule Poirot are other detective characters from shows.",
      "answer": "a"
    },
    {
      "question_id": 3,
      "question": "What is the man doing in the video?",
      "choices": ["a) walking in a street", "b) walking indoors", "c) investigating a scene", "d) leaving a scene"],
      "justification": "the man is investigating the scene ({3}). The options walking in a street, and walking indoors are general descriptions but not specific enough to the contents of the video, and leaving a scene is the opposite of investigating.",
      "answer": "c"
    },
    {
      "question_id": 4,
      "question": "Where is the video taking place?",
      "choices": ["a) house", "b) basement", "c) street", "d) crime scene"],
      "justification": "the video is taking place in a crime scene ({4}). The other provided options are common places, but not as specific as a crime scene.",
      "answer": "d"
    },
    {
      "question_id": 5,
      "question": "Which street appears in the video?",
      "choices": ["a) Liverpool", "b) Baker", "c) Oxford", "d) Bond"],
      "justification": "the street appearing in the video is the Baker Street ({5}). The options Liverpool, Baker, Oxford and Bond are different names of streets.",
      "answer": "b"
    },
    {
      "question_id": 6,
      "question": "What is the perspective of the video?",
      "choices": ["a) close up", "b) forced", "c) farther away", "d) top down"],
      "justification": "the perspective of the video is forced. The other options are other perspective styles in video.",
      "answer": "b"
    }
  ]
}

Description:

Larry David costumed as Bob Ross is drawing a nature scene but spills the paint

Answer:

{
  "keywords": "{1}[Larry David, entity, 1.0] as {2}[Bob Ross, entity, 1.0] {3}[is drawing, action, 1.0] a {4}[nature scene, object, 1.0] {5}[but, temporal relation, 1.0] {6}[spills, spatial relation, 1.0], {7}[the paint, object, 1.0]",
  "qas": [
    {
      "question_id": 1,
      "question": "Who is the character that draws a painting in the video?",
      "choices": ["a) Bob Ross", "b) Larry David", "c) Bill Alexander", "d) George Costanza"],
      "justification": "Larry David is present in the video ({1}). The option Bob Ross is the person that Larry is dressed as, Bill Alexander is a painter with similar style as Bob Ross, and George Costanza is a character similar to Larry David.",
      "answer": "b"
    },
    {
      "question_id": 2,
      "question": "Who is the painter of the video dressed as?",
      "choices": ["a) Bill Alexander", "b) William Alexander", "c) Thomas Kinkade", "d) Bob Ross"],
      "justification": "the main character is dressed like Bob Ross ({2}). The other options are all painters that are similar to Bob Ross.",
      "answer": "d"
    },
    {
      "question_id": 3,
      "question": "What is the painter doing in the video?",
      "choices": ["a) looking at a painting", "b) sitting next to a painting", "c) drawing a painting", "d) hanging up a painting"],
      "justification": "the man is drawing a painting ({3}). The other options are still involving a painting; looking at and sitting next to a painting are more static, and hanging up a painting is a different action from drawing the painting.",
      "answer": "c"
    },
    {
      "question_id": 4,
      "question": "What is depicted in the painting in the video?",
      "choices": ["a) nature scene", "b) abstract art", "c) geometric shapes", "d) blank canvas"],
      "justification": "the painting in the video depicts a nature scene ({4}). The other options are all different types of paintings that are mutually exclusive with depicting a nature scene.",
      "answer": "a"
    },
    {
      "question_id": 5,
      "question": "What is happening in the end of the video?",
      "choices": ["a) the man looks at the painting", "b) the man spills the paint", "c) the main draws the painting", "d) the man leaves the painting"],
      "justification": "towards the end of the video the man spills the paint ({5}, {6}). The option of drawing the painting happens earlier in the video, and the other two options are alternative actions around the painting.",
      "answer": "b"
    },
    {
      "question_id": 6,
      "question": "What does the man overturn in the end of the video?",
      "choices": ["a) the paint", "b) the painting", "c) the hat", "d) the brushes"],
      "justification": "the man overturns the paint. The option of the painting is another object present in the video, but not the correct one given the question, and the hat and brushes are related objects that are likely in the space in the video.",
      "answer": "a"
    }
  ]
}

Description:

Child swings high on tire swing

Answer:

{
  "keywords": "{1}[Child, entity, 1.0] {2}[swings, action, 1.0] {3}[high, spatial relation, 1.0] {4}[on tire swing, spatial relation, 1.0]",
  "qas": [
    {
      "question_id": 1,
      "question": "What is the age of the character in the video?",
      "choices": ["a) child", "b) young man", "c) baby", "d) old man"],
      "justification": "the main character of the video is a child ({1}). The options young man, baby and old man are characters of different ages.",
      "answer": "a"
    },
    {
      "question_id": 2,
      "question": "What is the child doing in the video?",
      "choices": ["a) sits on swing", "b) pushes the swing", "c) swings on swing", "d) walks away from the swing"],
      "justification": "the child swings on the swing ({2}). The option sits on the swing is similar, but it does not have any movement. The options pushes the swing and walks away from the swing require a different position of the child relative to the swing.",
      "answer": "c"
    },
    {
      "question_id": 3,
      "question": "What is the child doing on the swing?",
      "choices": ["a) sits", "b) swings high", "c) moves slightly", "d) gets off"],
      "justification": "the child swings high on the swing ({3}). The options sits and moves slightly are different movements of different intensity that the child could have been doing on the swing and the option gets off the swing is the opposite.",
      "answer": "b"
    },
    {
      "question_id": 4,
      "question": "Where is the child sitting on?",
      "choices": ["a) circular swing", "b) flat swing", "c) classic swing", "d) tire swing"],
      "justification": "The child sits in a tire swing ({4}). The other options are all different types of swings that are similar to tire swing.",
      "answer": "d"
    }
  ]
}

Description:

Frog jumps in a pond, forced perspective

Answer:

{
  "keywords": "{1}[Frog, entity, 1.0] {2}[jumps, action, 1.0] {3}[in a pond, spatial relation, 1.0] {4}[forced perspective, style, 1.0]",
  "qas": [
    {
      "question_id": 1,
      "question": "What animal is present in the video?",
      "choices": ["a) toad", "b) salamander", "c) frogs", "d) frog"],
      "justification": "the animal of the video is a frog ({1}). The option frogs is the plural which is not correct given the description. The options salamander and toad are animals similar to frog.",
      "answer": "d"
    },
    {
      "question_id": 2,
      "question": "What is the frog doing in the video?",
      "choices": ["a) sits next to a pond", "b) jumps in a pond", "c) jumps out of a pond", "d) slides in a pond"],
      "justification": "the frog jumps in a pond ({2}). The option sits next to a pond is related to the pond, but it does not have any movement. The option slides in a pond has a similar movement but it is a different action of different intensity. The option jumps out of a pond is the opposite.",
      "answer": "b"
    },
    {
      "question_id": 3,
      "question": "Where is the frog jumping in?",
      "choices": ["a) lake", "b) reservoir", "c) pond", "d) fountain"],
      "justification": "the frog jumps in a pond ({3}). The other options are all different types of water masses of different sizes.",
      "answer": "c"
    },
    {
      "question_id": 4,
      "question": "What is the perspective that the video is filmed?",
      "choices": ["a) aerial perspective", "b) forced perspective", "c) linear perspective", "d) one point perspective"],
      "justification": "the video is filmed in a forced perspective. The other options are all different perspective styles in video.",
      "answer": "b"
    }
  ]
}

Description:
{prompt}
Answer:
"""

RUBRIC_VALIDATOR_PROMPT = """
# Instructions
Watch the video below carefully and answer the question based on the choices
provided. Only answer with the letter (a, b, c, or d) that corresponds to the
correct answer.

{rubrics}

# Video
{video}

# Output Format
<question>
Question: repeat the original question
Verdict: a|b|c|d|e
</question>
"""