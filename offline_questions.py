"""Bundled question pack so the game can start without an API key."""


def is_valid_question_pack(data: object) -> bool:
    if not isinstance(data, dict):
        return False
    for key in ("round1", "round2"):
        rounds = data.get(key)
        if not isinstance(rounds, list) or len(rounds) < 6:
            return False
        for cat in rounds[:6]:
            if not isinstance(cat, dict):
                return False
            qs = cat.get("questions")
            if not isinstance(qs, list) or len(qs) < 5:
                return False
            for q in qs[:5]:
                if not isinstance(q, dict):
                    return False
                options = q.get("options")
                if not isinstance(options, list) or len(options) < 3:
                    return False
    round3 = data.get("round3")
    if not isinstance(round3, list) or not round3:
        return False
    final_cat = round3[0]
    if not isinstance(final_cat, dict):
        return False
    final_qs = final_cat.get("questions")
    return isinstance(final_qs, list) and bool(final_qs)


def _q(value: int, question: str, options: list[str], correct: int) -> dict:
    return {"value": value, "question": question, "options": options, "correct": correct}


def _cat(name: str, questions: list[dict]) -> dict:
    return {"name": name, "questions": questions}


def load_offline_questions() -> dict:
    r1 = [200, 400, 600, 800, 1000]
    r2 = [400, 800, 1200, 1600, 2000]

    science_1 = [
        _q(r1[0], "What gas do plants absorb for photosynthesis?", ["Oxygen", "Carbon dioxide", "Nitrogen"], 1),
        _q(r1[1], "What is the chemical symbol for gold?", ["Au", "Ag", "Gd"], 0),
        _q(r1[2], "How many planets are in the Solar System?", ["7", "8", "9"], 1),
        _q(r1[3], "What particle has a negative charge?", ["Proton", "Neutron", "Electron"], 2),
        _q(r1[4], "What is H2O better known as?", ["Hydrogen peroxide", "Water", "Salt"], 1),
    ]
    history_1 = [
        _q(r1[0], "Who was the first President of the United States?", ["Abraham Lincoln", "George Washington", "Thomas Jefferson"], 1),
        _q(r1[1], "In which year did World War II end?", ["1943", "1945", "1948"], 1),
        _q(r1[2], "The Great Wall is primarily in which country?", ["Japan", "Mongolia", "China"], 2),
        _q(r1[3], "Which empire built the Colosseum?", ["Greek", "Roman", "Ottoman"], 1),
        _q(r1[4], "Who was known as the Maid of Orleans?", ["Cleopatra", "Joan of Arc", "Queen Victoria"], 1),
    ]
    literature_1 = [
        _q(r1[0], "Who wrote Romeo and Juliet?", ["Charles Dickens", "William Shakespeare", "Jane Austen"], 1),
        _q(r1[1], "What is the boy wizard's last name in the famous series?", ["Potter", "Weasley", "Granger"], 0),
        _q(r1[2], "Who wrote Pride and Prejudice?", ["Emily Bronte", "Jane Austen", "Mary Shelley"], 1),
        _q(r1[3], "In which language was Don Quixote originally written?", ["French", "Italian", "Spanish"], 2),
        _q(r1[4], "Who wrote The Odyssey?", ["Homer", "Virgil", "Sophocles"], 0),
    ]
    geography_1 = [
        _q(r1[0], "What is the capital of France?", ["Lyon", "Paris", "Marseille"], 1),
        _q(r1[1], "Which ocean is the largest?", ["Atlantic", "Indian", "Pacific"], 2),
        _q(r1[2], "Mount Everest lies on the border of Nepal and which country?", ["India", "China", "Bhutan"], 1),
        _q(r1[3], "Which desert is the largest hot desert on Earth?", ["Gobi", "Sahara", "Kalahari"], 1),
        _q(r1[4], "What is the longest river in the world by many modern measures?", ["Nile", "Amazon", "Yangtze"], 1),
    ]
    film_1 = [
        _q(r1[0], "Which movie features a hobbit named Frodo?", ["Harry Potter", "The Lord of the Rings", "Narnia"], 1),
        _q(r1[1], "Who directed Jurassic Park?", ["James Cameron", "Steven Spielberg", "George Lucas"], 1),
        _q(r1[2], "What is the name of the clownfish in Finding Nemo?", ["Marlin", "Nemo", "Dory"], 1),
        _q(r1[3], "Which film won Best Picture at the 1994 Oscars?", ["Forrest Gump", "Pulp Fiction", "The Lion King"], 0),
        _q(r1[4], "Who played Jack in Titanic?", ["Brad Pitt", "Leonardo DiCaprio", "Matt Damon"], 1),
    ]
    math_1 = [
        _q(r1[0], "What is 7 times 8?", ["54", "56", "64"], 1),
        _q(r1[1], "What is the square root of 81?", ["8", "9", "10"], 1),
        _q(r1[2], "How many degrees are in a right angle?", ["45", "90", "180"], 1),
        _q(r1[3], "What is the value of pi rounded to two decimals?", ["3.12", "3.14", "3.16"], 1),
        _q(r1[4], "What is 2 to the power of 5?", ["16", "32", "64"], 1),
    ]

    science_2 = [
        _q(r2[0], "What is the powerhouse of the cell?", ["Nucleus", "Mitochondrion", "Ribosome"], 1),
        _q(r2[1], "Which scientist proposed the three laws of motion?", ["Einstein", "Newton", "Galileo"], 1),
        _q(r2[2], "What is the most abundant gas in Earth's atmosphere?", ["Oxygen", "Carbon dioxide", "Nitrogen"], 2),
        _q(r2[3], "What does DNA stand for?", ["Deoxyribonucleic acid", "Dinucleic acetate", "Dioxin nucleic assembly"], 0),
        _q(r2[4], "Which planet has the Great Red Spot?", ["Mars", "Jupiter", "Saturn"], 1),
    ]
    history_2 = [
        _q(r2[0], "The Magna Carta was signed in which century?", ["11th", "13th", "15th"], 1),
        _q(r2[1], "Who was the British prime minister for most of World War II?", ["Chamberlain", "Churchill", "Attlee"], 1),
        _q(r2[2], "Which civilization used cuneiform writing?", ["Maya", "Sumerian", "Inca"], 1),
        _q(r2[3], "The fall of Constantinople occurred in which year?", ["1453", "1492", "1517"], 0),
        _q(r2[4], "Who led the Indian independence movement with nonviolent resistance?", ["Nehru", "Gandhi", "Jinnah"], 1),
    ]
    literature_2 = [
        _q(r2[0], "Which novel begins with 'Call me Ishmael'?", ["Moby-Dick", "Dracula", "Frankenstein"], 0),
        _q(r2[1], "Who wrote 1984?", ["Aldous Huxley", "George Orwell", "Ray Bradbury"], 1),
        _q(r2[2], "In Dante's Inferno, how many circles of Hell are described?", ["7", "9", "12"], 1),
        _q(r2[3], "Which poet wrote 'Ode to a Nightingale'?", ["Keats", "Byron", "Shelley"], 0),
        _q(r2[4], "Who created the detective Hercule Poirot?", ["Arthur Conan Doyle", "Agatha Christie", "Dorothy Sayers"], 1),
    ]
    geography_2 = [
        _q(r2[0], "What is the capital of Canada?", ["Toronto", "Ottawa", "Vancouver"], 1),
        _q(r2[1], "Which African country has the largest population?", ["Egypt", "Nigeria", "South Africa"], 1),
        _q(r2[2], "The Strait of Gibraltar separates Spain from which continent?", ["Asia", "Africa", "South America"], 1),
        _q(r2[3], "Which US state has the most coastline?", ["California", "Florida", "Alaska"], 2),
        _q(r2[4], "Lake Baikal is located in which country?", ["China", "Russia", "Kazakhstan"], 1),
    ]
    film_2 = [
        _q(r2[0], "Which 2010 film is set inside a dream-sharing technology?", ["Inception", "Interstellar", "The Matrix"], 0),
        _q(r2[1], "Who composed the score for Star Wars?", ["Hans Zimmer", "John Williams", "Howard Shore"], 1),
        _q(r2[2], "Which studio made Spirited Away?", ["Pixar", "Studio Ghibli", "DreamWorks"], 1),
        _q(r2[3], "In Casablanca, what is the name of the nightclub?", ["Rick's Cafe Americain", "The Blue Parrot", "Cafe Moulin"], 0),
        _q(r2[4], "Who directed Parasite (2019)?", ["Bong Joon-ho", "Park Chan-wook", "Lee Chang-dong"], 0),
    ]
    math_2 = [
        _q(r2[0], "What is the next prime after 13?", ["15", "17", "19"], 1),
        _q(r2[1], "What is the derivative of x^2?", ["x", "2x", "x^2"], 1),
        _q(r2[2], "How many sides does a dodecagon have?", ["10", "12", "20"], 1),
        _q(r2[3], "What is the sum of interior angles of a triangle?", ["90 degrees", "180 degrees", "360 degrees"], 1),
        _q(r2[4], "What is the Fibonacci number after 8, if the sequence is 1,1,2,3,5,8,...?", ["11", "13", "16"], 1),
    ]

    return {
        "round1": [
            _cat("Science", science_1),
            _cat("History", history_1),
            _cat("Literature", literature_1),
            _cat("Geography", geography_1),
            _cat("Film", film_1),
            _cat("Math", math_1),
        ],
        "round2": [
            _cat("Science", science_2),
            _cat("History", history_2),
            _cat("Literature", literature_2),
            _cat("Geography", geography_2),
            _cat("Film", film_2),
            _cat("Math", math_2),
        ],
        "round3": [
            _cat(
                "Science",
                [
                    _q(
                        2000,
                        "Which constant is approximately 6.626 x 10^-34 joule-seconds?",
                        ["Avogadro's number", "Planck's constant", "Boltzmann's constant"],
                        1,
                    )
                ],
            )
        ],
    }
