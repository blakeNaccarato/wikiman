Don't put a heading at the top of your Markdown files. GitHub Wiki automatically generates the title at the top of every wiki page. Dashes are replaced by spaces in the filename (e.g. `Wiki-Page.md` to "Wiki Page") and the title is presented above your content. If you're linting your Markdown documentation, you may need to disable a warning about missing a heading on the first line.

If you're using the [markdownlint] extension in VSCode, you can disable the `first-line-heading` warning by inserting the following into your `settings.json`.

```json
// settings.json
{
    // ... other settings

    "markdownlint.config": {
        "first-line-heading": false
    },

    // ... other settings
}
```

[markdownlint]: https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint

## Don't rename `Home.md`

GitHub Wikis requires a `Home.md` file to be in your project. This serves as the home page, and it cannot be named differently. This, coupled with the fact that page titles are generated from Markdown filenames, means that every GitHub Wiki has "Home" at its root.

## Try not to use first-level headings (#) at all

This advice may be classified as a matter of preference, but I don't recommend using first-level headings (lines prefixed by a single "#") *at all*. This has to do with the size at which first-level headings are rendered by GitHub Wiki, compared with that of the page title.

## Wikiman generates tables of contents

Wikiman can generate a table of contents (TOC) in the sidebar of every wiki page in your wiki. You instruct it to do so by executing `wikiman update` or `wm up` at the command-line. It finds the highest-priority heading level in your files, and links to those top-level headings sequentially in the sidebar. Because GitHub Wiki does not have a fancy scrolling sidebar that stays near your position in the page, a full-fledged TOC is not so useful. Additionally, nesting beyond one or two indentation levels gets ugly in the sidebar, so it is easier to keep the TOC "flat". This is another point where Wikiman is a bit opinionated, as it won't generate deeper headings in the TOC.

### This is a third-level heading

There are no first-level headings on this page. So the second-level headings get reported in the TOC, and any heading levels deeper than that are not linked. So you can get to the heading titled "**Now, onto Wikiman**", but not "**This is a third-level heading**", for example.

#### This is a fourth-level heading

This heading won't appear in the TOC, either.

## Wrapping up

If you've read `README.md` in the main Wikiman project repo, and you've read this page here, then you know all you need to know about GitHub Wikis. It is a quirky little platform, but it works well enough for certain projects. We have to live with some of the quirks, such as the mandatory `Home.md`. But Wikiman helps overcome some of the others.

The rest of this wiki contains randomly-generated page names with a variety of different contents. This wiki is used as the testing ground for Wikiman. Tests are written with `pytest`. Each function that operates directly on the folder structure of the wiki can be tested if the inital state and expected result are known. Some `pytest` fixtures are used to help with setup and teardown of initial/expected wiki states.
