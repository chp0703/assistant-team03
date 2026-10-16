
# Lab 02 - UI Source Citation Design

## 1. Overview

This document describes how the Study Assistant user
interface should display sources below its answers.

The goal is to help users understand where information
comes from and make it easier to verify the answers.

This document provides two UI mockups. It does not
implement automatic source retrieval or citation generation.

## 2. Citation Display Design

Each assistant response should contain:

- The answer to the user's question.
- A "Sources" section below the answer.
- The title or name of each information source.
- An optional reference such as a URL, file, or data record.

### Display Rules

1. Sources appear directly below the assistant's answer.
2. Each source has a clear and readable label.
3. Source URLs are clickable when valid URLs are available.
4. Sources must refer to information actually used by the backend.
5. If no verified source is available, the UI must not
   invent a citation.

## 3. Mockup Example 1 - Office Information

### User Question

Where is the Training Office?

### Proposed Assistant Response

The Training Office is located in Room [example room].

**Sources:**
- [1] `data/offices.csv` - Training Office record

### UI Mockup

    +--------------------------------------------------+
    | User                                             |
    | Where is the Training Office?                    |
    +--------------------------------------------------+
    | Study Assistant                                  |
    | The Training Office is located in                |
    | Room [example room].                             |
    |                                                  |
    | Sources:                                         |
    | [1] data/offices.csv - Training Office record     |
    +--------------------------------------------------+

### Explanation

This example shows a source reference to an internal
CSV file used for office lookup.

The room is a placeholder in this design mockup,
not a verified office location.

## 4. Mockup Example 2 - Opening Hours

### User Question

When does the Library open?

### Proposed Assistant Response

The Library opening hours are [example opening hours].

**Sources:**
- [1] `data/offices.csv` - Library record

### UI Mockup

    +--------------------------------------------------+
    | User                                             |
    | When does the Library open?                      |
    +--------------------------------------------------+
    | Study Assistant                                  |
    | The Library opening hours are                    |
    | [example opening hours].                         |
    |                                                  |
    | Sources:                                         |
    | [1] data/offices.csv - Library record             |
    +--------------------------------------------------+

### Explanation

This example illustrates how the UI could show the
data source used to provide opening-hour information.

The opening hours are placeholders and must be
replaced with actual verified data when implemented.

## 5. Planned Data Structure

A future backend response could return structured data:

    {
      "answer": "Example assistant answer",
      "sources": [
        {
          "title": "Office directory",
          "reference": "data/offices.csv"
        }
      ]
    }

This is a proposed design, not the current backend format.

The existing `reply(message)` function currently returns
a plain string and does not provide structured citations.

## 6. Future Implementation

1. Extend the backend to provide source information.
2. Return an answer together with relevant source metadata.
3. Render the answer in the chat message area.
4. Display source references underneath the answer.
5. Handle responses without verified sources.
6. Test the citation display using different questions.

## 7. Acceptance Criteria

- [x] Citation display design is documented.
- [x] Two example mockups are included.
- [x] Sources appear below assistant answers.
- [x] The proposed design is distinguished from
      the current backend implementation.

## 8. Related Issue

GitHub Issue #10 - UI: show sources under each answer.