// ============================================================
// Matplotlib Training Book Template (Typst 0.15+)
// ============================================================

// Page setup
#let page-setup() = {
  set page(
    paper: "a4",
    margin: (top: 2.5cm, bottom: 2.5cm, left: 3cm, right: 2.5cm),
    numbering: "1",
    number-align: center,
  )
  set text(font: ("Libertinus Serif", "Times New Roman"), size: 11pt, lang: "en")
  set par(justify: true, leading: 0.45em)
}

// Heading styling
#let heading-style() = {
  set heading(numbering: "1.1")
  show heading.where(level: 1): it => {
    block(below: 1.5em, above: 2.5em)[
      #text(size: 24pt, weight: "bold", fill: rgb("#1a3a5c"), it)
      #line(length: 100%, stroke: 0.5pt + rgb("#1a3a5c"))
    ]
  }
  show heading.where(level: 2): it => {
    block(below: 1em, above: 1.8em)[
      #text(size: 18pt, weight: "bold", fill: rgb("#2a5a8c"), it)
    ]
  }
  show heading.where(level: 3): it => {
    block(below: 0.8em, above: 1.2em)[
      #text(size: 14pt, weight: "semibold", fill: rgb("#3a7ab5"), it)
    ]
  }
}

// Code block styling
#let code-style() = {
  show raw.where(block: true): it => {
    block(
      fill: luma(240),
      inset: 12pt,
      radius: 4pt,
      width: 100%,
      stroke: 0.5pt + luma(200),
    )[
      #set text(font: ("Fira Code", "Cascadia Code", "Courier New"), size: 9pt)
      #it
    ]
  }
  show raw.where(block: false): it => {
    set text(font: ("Fira Code", "Cascadia Code", "Courier New"), size: 9pt)
    box(fill: luma(240), inset: (x: 4pt, y: 2pt), radius: 2pt)[#it]
  }
}

// Figure caption
#let figure-caption() = {
  show figure.caption: it => {
    align(center, text(size: 9pt, fill: luma(120), it))
  }
}

// Header and footer
#let header-footer() = {
  show page: it => {
    block(
      above: 0pt,
      below: 6pt,
      width: 100%,
    )[
      #if it.numbering != none and it.number > 1 {
        set text(size: 8pt, fill: luma(150))
        align(right, it.heading)
      }
    ]
    it
  }
}

// Title page
#let title-page(title, subtitle, author, date) = {
  block(height: 100%, width: 100%)[
    #set align(center)
    #set text(size: 36pt, weight: "bold", fill: rgb("#1a3a5c"))
    #block(above: 30%, [#title])
    #set text(size: 20pt, weight: "regular", fill: rgb("#3a7ab5"))
    #block(above: 0.5em, [#subtitle])
    #line(length: 40%, stroke: 1pt + rgb("#1a3a5c"))
    #set text(size: 12pt, fill: luma(100))
    #block(above: 2em, [#author])
    #block(above: 0.3em, [#date])
    #block(above: 4em)[
      #set text(size: 10pt, fill: luma(150))
      A comprehensive guide to creating publication-quality \
      data visualizations with Python and Matplotlib
    ]
  ]
}

// Main book template
#let book-template(
  title: none,
  subtitle: none,
  author: none,
  date: none,
  body,
) = {
  page-setup()
  heading-style()
  code-style()
  figure-caption()

  title-page(title, subtitle, author, date)
  pagebreak()

  set text(size: 11pt)
  heading(level: 1, outlined: false)[Table of Contents]
  outline(indent: auto, depth: 2)
  pagebreak()

  body

  pagebreak()
  heading(level: 1, outlined: false)[References]
  bibliography("references.bib", title: none, style: "ieee")
}
