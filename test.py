from promptsbot import FormattedPrompts

def FormattedPromptsTest():
	print(FormattedPrompts(-1, 1))
	print(FormattedPrompts(1, 1))
	print(FormattedPrompts(0, 1))
	print(FormattedPrompts(2, 2))
	print(FormattedPrompts(10, 10))
	print(FormattedPrompts(10, -1))
	print(FormattedPrompts(1000000, 2))

if __name__ == '__main__':
	FormattedPromptsTest()