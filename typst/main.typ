#import "template.typ": *

// Book metadata
#let book-title = "Matplotlib Training"
#let book-subtitle = "From Zero to Publication-Quality Visualizations"
#let book-author = "Birhanu Asmerom, Department of Physics, Wollo University"
#let book-date = "2024"

// Apply template
#show: book-template.with(
  title: book-title,
  subtitle: book-subtitle,
  author: book-author,
  date: book-date,
)

// Include all chapters
#include "chapters/00-preface.typ"
#include "chapters/01-introduction.typ"
#include "chapters/02-setup.typ"
#include "chapters/03-jupyter.typ"
#include "chapters/04-matplotlib-basics.typ"
#include "chapters/05-basic-charts.typ"
#include "chapters/06-styling.typ"
#include "chapters/07-axes.typ"
#include "chapters/08-subplots.typ"
#include "chapters/09-statistical.typ"
#include "chapters/10-scientific.typ"
#include "chapters/11-timeseries.typ"
#include "chapters/12-geographic.typ"
#include "chapters/13-numpy-pandas.typ"
#include "chapters/14-advanced.typ"
#include "chapters/15-publication.typ"
#include "chapters/16-projects.typ"
#include "chapters/17-capstone.typ"
#include "chapters/99-appendix.typ"