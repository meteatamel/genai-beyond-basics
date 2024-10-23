# Reference: https://llm-guard.com/input_scanners/ban_code/
def ban_code():
    from llm_guard.input_scanners import BanCode

    prompt = "System.out.println('Hello World')"
    scanner = BanCode()
    prompt, is_valid, risk_score = scanner.scan(prompt)

    print_results(is_valid, prompt, risk_score)


def print_results(is_valid, prompt, risk_score):
    print(f"Prompt: {prompt}")
    print(f"Valid? {is_valid}")
    print(f"Risk score: {risk_score}")


# Reference: https://llm-guard.com/input_scanners/ban_competitors/
def ban_competitors():
    from llm_guard.input_scanners import BanCompetitors

    prompt = "What are some serverless products in AWS?"
    competitor_list = ["AWS", "Azure"]
    scanner = BanCompetitors(competitors=competitor_list, redact=False, threshold=0.5)
    prompt, is_valid, risk_score = scanner.scan(prompt)

    print_results(is_valid, prompt, risk_score)


def ban_substrings():
    from llm_guard.input_scanners import BanSubstrings
    from llm_guard.input_scanners.ban_substrings import MatchType

    prompt = "JP Morgan has an office in London"
    banned_strings = [
        "Acorns",
        "Citigroup",
        "Citi",
        "Fidelity Investments",
        "Fidelity",
        "JP Morgan Chase and company",
        "JP Morgan",
        "JP Morgan Chase",
        "JPMorgan Chase",
        "Chase" "M1 Finance",
        "Stash Financial Incorporated",
        "Stash",
        "Tastytrade Incorporated",
        "Tastytrade",
        "ZacksTrade",
        "Zacks Trade",
    ]
    scanner = BanSubstrings(
        substrings=banned_strings,
        match_type=MatchType.STR,
        case_sensitive=False,
        redact=True,
        contains_all=False,
    )
    sanitized_prompt, is_valid, risk_score = scanner.scan(prompt)

    print_results(is_valid, prompt, risk_score)


def main():
    ban_code()
    ban_competitors()
    ban_substrings()


if __name__ == '__main__':
    main()
