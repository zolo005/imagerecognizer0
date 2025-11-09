"""Simple CLI AI assistant.

Features:
- Local rule-based mode (default) for answering basic questions and commands.
- Optional OpenAI integration when OPENAI_API_KEY environment variable is set.
- Conversation history, help, and simple commands: /help, /exit, /history, /mode

Run: python main.py
"""
from __future__ import annotations

import os
import sys
import json
try:
	import readline
except Exception:
	# readline is not available on some platforms (notably Windows)
	readline = None
from typing import List, Dict, Optional

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")


class Assistant:
	def __init__(self, use_openai: bool = False):
		self.history: List[Dict[str, str]] = []
		self.use_openai = use_openai and OPENAI_KEY is not None

		if use_openai and OPENAI_KEY is None:
			print("OPENAI_API_KEY not found in environment; falling back to local mode.")

		if self.use_openai:
			try:
				import openai

				openai.api_key = OPENAI_KEY
				self._openai = openai
			except Exception as e:
				print(f"Failed to import OpenAI client: {e}. Falling back to local mode.")
				self.use_openai = False

	def add_user(self, text: str) -> None:
		self.history.append({"role": "user", "text": text})

	def add_assistant(self, text: str) -> None:
		self.history.append({"role": "assistant", "text": text})

	def answer(self, prompt: str) -> str:
		self.add_user(prompt)
		if self.use_openai:
			resp = self._ask_openai(prompt)
		else:
			resp = self._local_answer(prompt)

		self.add_assistant(resp)
		return resp

	def _local_answer(self, prompt: str) -> str:
		# Very small rule-based responder for demonstration
		lp = prompt.lower().strip()
		if lp in ("hi", "hello", "hey"):
			return "Hello! I am your local assistant. Ask me to do something or type /help for commands."
		if lp.startswith("what is your name") or lp.startswith("who are you"):
			return "I'm a small CLI assistant. You can run me with an OpenAI key to use the OpenAI API."
		if lp.startswith("time") or "time" in lp:
			from datetime import datetime

			return f"Current time: {datetime.now().isoformat()}"
		if lp.startswith("echo "):
			return prompt[5:]
		if lp in ("help", "/help"):
			return self._help_text()
		if lp in ("history", "/history"):
			return json.dumps(self.history[-10:], indent=2)
		# fallback: simple transformation
		return "I don't know that yet. Try /help or run with OPENAI_API_KEY for smarter answers."

	def _help_text(self) -> str:
		return (
			"Commands:\n"
			"  /help        Show this help\n"
			"  /exit        Exit the assistant\n"
			"  /history     Show the last interactions (JSON)\n"
			"  /mode        Show current mode (local or openai)\n"
			"You can also ask normal questions. Prefix with 'echo ' to echo text."
		)

	def _ask_openai(self, prompt: str) -> str:
		# Minimal wrapper around OpenAI chat completion. Uses gpt-3.5-turbo if available.
		model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
		try:
			messages = [{"role": h["role"], "content": h["text"]} for h in self.history]
			messages.append({"role": "user", "content": prompt})
			res = self._openai.ChatCompletion.create(model=model, messages=messages, max_tokens=300)
			text = res["choices"][0]["message"]["content"].strip()
			return text
		except Exception as e:
			return f"OpenAI request failed: {e}"


def repl():
	use_openai = bool(OPENAI_KEY)
	a = Assistant(use_openai=use_openai)

	print("Small CLI AI assistant. Type /help for commands. (Ctrl-D or /exit to quit)")
	if use_openai:
		print("OpenAI mode enabled.")

	try:
		while True:
			try:
				s = input("> ")
			except EOFError:
				print()
				break

			if not s:
				continue
			cmd = s.strip()

			if cmd in ("/exit", "exit"):
				break
			if cmd in ("/help", "help"):
				print(a._help_text())
				continue
			if cmd in ("/history", "history"):
				print(json.dumps(a.history, indent=2))
				continue
			if cmd in ("/mode", "mode"):
				print("openai" if a.use_openai else "local")
				continue

			out = a.answer(cmd)
			print(out)

	except KeyboardInterrupt:
		print()


if __name__ == "__main__":
	repl()

