import gpt_function as gpt
import midjourney as mid

# Test the function
theme = "马上鞭"
description = gpt.generate_description(theme)
print(description)
base_image_link = gpt.generate_link(theme)
print(base_image_link)
image_link = mid.generate_image(base_image_link,description)

print(image_link)