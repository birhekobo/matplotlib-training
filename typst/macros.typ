#let note-box(body) = {
  block(
    fill: luma(235), inset: 12pt, radius: 4pt, width: 100%,
    stroke: (left: 3pt + rgb("3a7ab5")),
  )[#text(size: 10pt, weight: "bold", fill: rgb("3a7ab5"))[Note: ] #body]
}
#let warning-box(body) = {
  block(
    fill: rgb("fbe9d9"), inset: 12pt, radius: 4pt, width: 100%,
    stroke: (left: 3pt + rgb("e87d2f")),
  )[#text(size: 10pt, weight: "bold", fill: rgb("e87d2f"))[Warning: ] #body]
}
#let info-box(body) = {
  block(
    fill: rgb("d9e6f2"), inset: 12pt, radius: 4pt, width: 100%,
    stroke: (left: 3pt + rgb("5a8fc7")),
  )[#text(size: 10pt, weight: "bold", fill: rgb("5a8fc7"))[Info: ] #body]
}
