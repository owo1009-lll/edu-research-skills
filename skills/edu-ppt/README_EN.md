# edu-ppt

[中文说明](README.md)

Turn your research or papers you are reading into a clear academic presentation.

## Usage

- “Present my paper in a 15-minute lab meeting.”
- “Make a research progress deck, keeping unfinished work explicit.”
- “Explain this English paper in a Chinese presentation.”
- “Find papers on infant socioemotional development and prepare slide text and speaker notes.”
- “Create an editable deck using this template.”

## Outputs

Content mode delivers actual slide copy, visual arrangements, narration, source locations and timing. Finished mode adds editable PPTX with embedded notes, PNG/PDF previews and checks. Own research distinguishes completed work, proposals and progress. Paper reading connects What, Why, How and Result.

## Dependencies and Boundaries

Python dependencies are in requirements.txt. The single engine is python-pptx; no extra model API key is required. Rendering needs Windows PowerPoint, or LibreOffice and pdftoppm. No renderer means no claimed visual acceptance. Text, tables, models and reconstructed charts use native objects; source images are not internally editable. Abstract access does not authorize invented full-text details, new analyses or progress claims.

See the [entrypoint](SKILL.md), [commands](references/production.md), [project references](references/open-source.md) and [synthetic and open-article examples](examples/README.md). Keep task materials under the user's edu_output/ppt directory, outside the skill.

## Status

- Beta: new module; development evals record automatic checks, AI review and scenario coverage separately. These are not author or expert acceptance.
