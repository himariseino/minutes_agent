---
marp: true
theme: default
paginate: true
backgroundColor: #fcfcfc
header: "Presentation Title"
footer: "Presenter Name"
style: |
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP&display=swap');
  section {
    font-family: 'Noto Sans JP', sans-serif;
  }
  :root {
    --base-color: #003366;
    --light-base: #005999;
    --figure-color: #F56B60;
    --figure-highlight: #20B2AA;
    --pale-base: #4D7999;
    --dark-base: #001F3F;
    --complement: #663300;
    --light-complement: #FF8000;
    --accent1: #FFCC00;
    --accent2: #00CC66;
    --background-color: #fcfcfc;
    --text-color: #333333;
  }
  code {
    background: #fcfcfc;
    padding: 0.1em 0.2em;
    border-radius: 0.2em;
  }
  h1 {
    color: var(--base-color);
  }
  h2 {
    color: var(--base-color);
  }
  a {
    color: var(--light-base);
  }
  strong {
    color: var(--dark-base);
  }
  .highlight {
    color: var(--light-complement);
  }
  .accent1 {
    color: var(--accent1);
  }
  .accent2 {
    color: var(--accent2);
  }
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
---

<!-- Title Slide -->

# Main Title

## Subtitle

Presenter Name
Date

---

<!-- Table Format -->

## Table Example

| Header 1 | Header 2 | Header 3 |
| :------: | :------: | :------: |
|  Cell 1  |  Cell 2  |  Cell 3  |
|  Cell 4  |  Cell 5  |  Cell 6  |
|  Cell 7  |  Cell 8  |  Cell 9  |

---

<!-- Code Block -->

## Code Example

```python
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
```

---

<!-- Bullet Points -->

## Key Points

- Main point 1
  - Sub-point A
  - Sub-point B
- Main point 2
  - Sub-point C
  - Sub-point D
- Main point 3

---

<!-- Eye-catching Slide -->
<!-- _class: lead -->

# Eye-catching Title

Impactful statement or question

---

<!-- Mid-summary (Centered title with bullet points) -->
<!-- _class: lead -->

## Mid-summary

- Key takeaway 1
- Key takeaway 2
- Key takeaway 3

---

<!-- Image Embedding (Full width) -->

## Full Width Image

![width:1000px center](https://via.placeholder.com/1000x500)

---

<!-- Image Embedding (Side by side) -->

## Side by Side Images

![bg left:50% width:400px](https://via.placeholder.com/400)
![bg right:50% width:400px](https://via.placeholder.com/400x300)

- Left image description
- Right image description

---

<!-- Image with Text (Right aligned image) -->

## Image with Text

![bg right:40%](https://via.placeholder.com/400x600)

- Point related to the image
- Another relevant point
- Third point explaining the concept

---

<!-- Quote Slide -->
<!-- _class: lead -->

> "The only way to do great work is to love what you do."
>
> -- Steve Jobs

---

<!-- Comparison Slide -->

## Comparison

| Feature | Option A | Option B |
| :------ | :------: | :------: |
| Cost    |    $$    |   $$$    |
| Speed   |   Fast   |  Faster  |
| Quality |   Good   |  Better  |

---

<!-- Timeline Slide -->

## Project Timeline

- 2023 Q1: Planning Phase
- 2023 Q2: Development Starts
- 2023 Q3: Beta Testing
- 2023 Q4: Product Launch
- 2024 Q1: Post-launch Review

---

<!-- Thank You Slide -->
<!-- _class: lead -->

# Thank You!

Any questions?

Contact: email@example.com
