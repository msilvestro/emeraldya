# Emeraldya

Create your own annotated translation from Japanese to English.

⚠️ This project is still in early development.

Look at the [Ririkon source code](https://github.com/msilvestro/ririkon/) to take inspiration from a working website.

## How to use

- Install the CLI with:
  ```shell
  poetry install
  ```
- Run the command with:
  ```shell
  emeraldya --input-dir input/ --output-dir output/ --template ririkon.html.jinja
  ```
  
## What are Emerald files?

Emerald is a markup specifically tailored for Japanese annotated translation such as the ones you can find on [Satori reader](https://www.satorireader.com/how-it-works).
Here is an example Emerald (`.em`) file:
```
--- header
title: 404
subtitle: Page not found

--- body
ページ^1 が 見つかりません -> Page not found

--- dictionary
ページ _ page
が _ indicates sentence subject (occasionally object) [particle]
見つかる みつかる to be found; to be discovered [godan verb]
見つかりません みつかりません ==> 見つかる negative polite form

--- notes
1: Modern Japanese terms are loan words from English, as in this case: ページ is literally the transliteration of "page" from the Latin alphabet to katakana.
```

It has four sections:
1. The **header** (`--- header`), that contains a list of arbitrary metadata that can be used to fill the template.
2. The **body** (`--- body`), that contains the Japanese text and the English translation (after the arrow ` -> `). You can also add notes adding a `^{something}` after a word (`{something}` can be any string). Notes can be added to multiple consecutive words, like `私^1 は^1 マッテオ^1 です^1`.
3. The **dictionary** (`--- dictionary`), that contains the definition of each word. The format is `{writing} {reading} {definition}`. If the reading is the same as the writing, you can leave a `_`. In the definition section, if you start with `==>` and then refer to another word, you will create a link (useful for verb conjugations, for instance).
4. The **notes** (`--- notes`, optional if no notes are present in the body), that contains the annotations to explain some peculiarities about a word or expression.


## How to customize templates

You need a [Jinja template](https://jinja.palletsprojects.com/en/3.1.x/templates/) that will be used to create the final HTML page with the data provided by an Emerald file. Take a look at the provided [Ririkon template](emeraldya/templates/ririkon.html.jinja) for reference, you can create yours starting from it.

## What's missing

As already said, this is in early development, I mostly created the bare minimum I needed for [Ririkon](https://ririkon.com).

This is what's missing:
- Support for different definitions for the same word
- A better characters splitter to assign furigana to kanjis (the implemented one will not work, for instance, on 連れて行く)
- Allow multiline Markdown strings for header fields and notes
- Raise useful errors
- Readable and exportable code
- Better documentation on Emerald files
- Tests
- A minimal template