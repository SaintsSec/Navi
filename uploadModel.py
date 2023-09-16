import os
import subprocess
import re

model_dir = os.path.expanduser("~/ssg/Zero/models")
models = [os.path.join(model_dir, f) for f in os.listdir(model_dir)]
model_count = len(models)

if model_count == 0:
    print(f"No models found in {model_dir}")
    exit(1)

print(f"Available models in {model_dir}:")
for i, model in enumerate(models):
    print(f"[{i}] {os.path.basename(model)}")

model_index = input(f"Select a model (0-{model_count-1}): ")

# Check if the input is a valid number
if not re.match("^[0-9]+$", model_index) or int(model_index) < 0 or int(model_index) >= model_count:
    print("Invalid selection. Please enter a valid number.")
    exit(1)

selected_model = models[int(model_index)]

data_payload = '{"model_file": "%s"}' % selected_model
curl_command = f'curl -X PUT http://0.0.0.0:5005/model -H "Content-Type: application/json" -d \'{data_payload}\''


print("Executing the following command:")
print(curl_command)

# Uncomment the line below to execute the curl command
subprocess.run(curl_command, shell=True)
print("Done!")
