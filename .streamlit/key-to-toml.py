import toml

output_file = ".streamlit/secrets.toml"

with open(".streamlit/service_account.json","r") as json_file:
    json_text = json_file.read()

config = {
    "textkey2": json_text
}
toml_config = toml.dumps(config)

with open(output_file, "a") as file:
    file.write(toml_config)