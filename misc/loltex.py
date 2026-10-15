#!/usr/bin/env python3
#
# This script guides you through setting up a basic latex document.
#
import os
import sys


def wait_for_yes_no(question):
    """Prompt the user with a yes/no question."""
    while True:
        answer = input(question + " (y/n): ").strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("Please enter 'y' or 'n'.")


class Greetings:
    def __init__(self):
        self.splash = r"""
----------------------------------------------
       _           _   _______  __   __
      | |         | | |__   __| \ \ / /
      | |     ___ | |    | | ___ \ V /
      | |    / _ \| |    | |/ _ \ > <
      | |___| (_) | |____| |  __// . \
      |______\___/|______|_|\___/_/ \_\

Welcome to LolTeXv0.4, the LaTeX setup script.
----------------------------------------------
"""
    def run(self):
        print(self.splash)
        return False


class LaTeXDocument:
    """Base class for LaTeX document creation."""

    def __init__(self, name, tex_file, compilation_file, bib_file=None):
        self.name = name
        self.tex_file = tex_file
        self.compilation_file = compilation_file
        self.bib_file = bib_file
        self.content_tex = ""
        self.content_compile = ""
        self.content_bib = ""

    def run(self):
        self._check_file_exists(self.tex_file)
        self._check_file_exists(self.compilation_file)
        if self.bib_file:
            self._check_file_exists(self.bib_file)

        self._write_file(self.tex_file, self.content_tex)
        self._write_file(self.compilation_file, self.content_compile)
        if self.bib_file:
            self._write_file(self.bib_file, self.content_bib)

        print(f"Created {self.tex_file}, {self.compilation_file}" +
              (f", {self.bib_file}" if self.bib_file else ""))
        return True

    def _check_file_exists(self, filename):
        """Check if a file exists and exit if it does."""
        if os.path.exists(filename):
            print(f"{filename} already exists. Exiting.")
            sys.exit(1)

    def _write_file(self, filename, content):
        """Write content to a file."""
        with open(filename, "w") as f:
            f.write(content.strip() + "\n")


class MakeBasicDocument(LaTeXDocument):
    """Creates a basic LaTeX document."""

    def __init__(self):
        super().__init__("basic LaTeX document", "document.tex", "compile.sh")
        self.content_tex = r"""
\documentclass[9pt,twocolumn]{scrartcl}

% ------------------------------------------------------------
% Packages
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage[a4paper]{geometry}
\geometry{margin=0.75in}
\usepackage{hyperref}
% ------------------------------------------------------------

% ------------------------------------------------------------
% Macros
\newcommand{\name}[0]{}
% ------------------------------------------------------------

% ------------------------------------------------------------
% Title information
\title{Fleeb}
\date{}
\author{Squanchy}
% ------------------------------------------------------------

\begin{document}

\maketitle

Here is some text

\end{document}
"""
        self.content_compile = r"""
#!/usr/bin/env bash
# -*- mode:sh; -*-

function compileAndClean {
    base_filename=$1
    # Compile LaTeX document
    pdflatex $base_filename

    # Remove auxiliary files
    rm $base_filename.aux $base_filename.log $base_filename.out

    # Make a backup copy of the pdf with today's date
    cp "$base_filename.pdf" "$base_filename-$(date '+%Y-%m-%d').pdf"
}

compileAndClean document
"""


class MakeDocumentWithReferences(LaTeXDocument):
    """Creates a LaTeX document with references."""

    def __init__(self):
        super().__init__("LaTeX document with references", "document.tex", "compile.sh", "references.bib")
        self.content_tex = r"""
\documentclass[9pt,twocolumn]{scrartcl}

% ------------------------------------------------------------
% Packages
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage[a4paper]{geometry}
\geometry{margin=0.75in}
\usepackage{hyperref}
\usepackage{natbib}
\bibliographystyle{plain}

% ------------------------------------------------------------
% Title information
\title{Fleeb with References}
\date{}
\author{Squanchy}
% ------------------------------------------------------------

\begin{document}

\maketitle

Here is some text with a citation \cite{sample}.

\bibliography{references}

\end{document}
"""
        self.content_compile = r"""
#!/usr/bin/env bash
# -*- mode:sh; -*-

function compileAndClean {
    base_filename=$1
    pdflatex $base_filename
    bibtex $base_filename
    pdflatex $base_filename
    pdflatex $base_filename
    rm $base_filename.aux $base_filename.log $base_filename.out $base_filename.bbl $base_filename.blg
    cp "$base_filename.pdf" "$base_filename-$(date '+%Y-%m-%d').pdf"
}

compileAndClean document
"""
        self.content_bib = r"""
@article{sample,
  author = {Doe, John},
  title = {An Example Paper},
  journal = {Journal of Examples},
  year = {2023},
  volume = {42},
  pages = {1--10}
}
"""


if __name__ == "__main__":
    greeter = Greetings()
    greeter.run()

    print("Please select an option:")
    print("  [1] Create a Basic LaTeX Document")
    print("  [2] Create a LaTeX Document with References")
    print("  [q] Quit")

    while True:
        choice = input("Enter your choice: ").strip().lower()
        if choice == "1":
            MakeBasicDocument().run()
            break
        elif choice == "2":
            MakeDocumentWithReferences().run()
            break
        elif choice == "q":
            print("Exiting without creating anything.")
            break
        else:
            print("Invalid choice, please try again.")
