# Wikiman

A CLI manager for GitHub Wikis. Manage pages and generate tree views, tables of contents, and relative navigation.

> NOTE: I am still implementing most of the features detailed [below]. If you are installing with `pip install wikiman`, then you will get version `0.3.0` and you can use `wikiman up` to update sidebars/footers, and `wikiman add ...` to add pages. I intend to implement aliases so that `wikiman update` and `wikiman up` will do the same thing, among others.

[below]: #CLI-usage

## Example

See the [wiki for Wikiman itself] to see the wiki that results from the usage example [detailed later on]. Note the Table of Contents in pages that are not empty. Also note the dynamic tree navigation in the sidebar and relative navigation in footers.

[wiki for Wikiman itself]: https://github.com/blakeNaccarato/wikiman/wiki

## Installation

**Wikiman** operates on a local clone of the GitHub wiki for your project. See [below][below2] for details.

```text
git clone https://github.com/user-name/repo-name.wiki.git
```

Install **Wikiman** either in your global Python environment or a virtual environment in the repo.

```text
pip install wikiman
```

**Wikiman** is opinionated about your wiki project structure in order to overcome the shortcomings built into GitHub wikis. This structure is [detailed later on].

[below2]: #Cloning-your-wiki-pages-in-order-to-use-Wikiman
[detailed later on]: #Wiki-project-structure-enforced-by-Wikiman

## CLI usage

*Update* sidebars and footers with tree views, relative navigation, and a table of contents. The following are equivalent

```text
wikiman update
wikiman up
```

*Add* a page "Measure Transient Respite" under "Impeach Vermilion Vacuum", after any other pages that are already there

```text
wikiman add Measure-Transient-Respite Impeach-Vermilion-Vacuum
```

*Insert* a page "Measure Transient Respite" under "Impeach Vermilion Vacuum", at the position specified. The following are equivalent

```text
wikiman add Measure-Transient-Respite Impeach-Vermilion-Vacuum 2
wikiman insert Measure-Transient-Respite Impeach-Vermilion-Vacuum 2
```

*Rename* a page "Measure Transient Respite" to "Middle Pasture Floating". The following are equivalent:

```text
wikiman rename Measure-Transient-Respite Middle-Pasture-Floating
wikiman rn Measure-Transient-Respite Middle-Pasture-Floating
```

*Remove* the page "Measure Transient Respite". The following are equivalent

```text
wikiman remove Measure-Transient-Respite
wikiman rm Measure-Transient-Respite
```

*Move* the page "Measure Transient Respite" (and its contents) under "Impeach Vermilion Vacuum", at the position specified. The following are equivalent

```text
wikiman move Measure-Transient-Respite Impeach-Vermilion-Vacuum 2
wikiman mv Measure-Transient-Respite Impeach-Vermilion-Vacuum 2
```

## Python script usage

You can also `import wikiman` to manage your wiki in Python scripts. **Wikiman** makes heavy use of `pathlib.Path` objects, only really handling `str` arguments at the CLI. The Python API documentation does not currently exist. It will be generated, along with sizable changes in the underlying Python logic, in the efforts detailed [below][below3].

[below3]: #What-comes-next?

## Case sensitivity and dashes in page titles

Pages can also be specified with spaces instead of dashes. Case is respected, with or without dashes, when *adding* a page, but a case insensitive match is made for pages in the second argument to the *add* or *move* options. The following are equivalent

```text
wikiman add Measure-Transient-Respite Impeach-Vermilion-Vacuum
wikiman add Measure-Transient-Respite impeach-vermilion-vacuum
wikiman add "Measure Transient Respite" impeach-vermilion-vacuum
wikiman add "Measure Transient Respite" "Impeach vermilion vacuum"
wikiman add "Measure Transient Respite" "impeach vermilion vacuum"
```

However, the following commands are different from the above and different to each other, as they will create the page with different case (commands truncated with ellipses)

```text
wikiman add measure-transient-respite ...
wikiman add Measure-transient-respite ...
wikiman add "MEASURE TRANSIENT RESPITE" ...
```

Your page titles cannot contain the following illegal characters: `\ / : * ? " < > |`.

> NOTE: Once the exception message has been finalized, I will add an example here.

GitHub Wikis automatically convert dashes to spaces in page titles. If you want an actual dash in your pages, consider using an *en dash* (–) instead. An *en dash* looks better with a space on either side of it. In the following equivalent examples, note that the slightly longer dash is an *en dash* which will actually show up in your page title on the web (commands truncated with ellipses)

```text
wikiman add Subject-–-A-bit-of-detail ...
wikiman add "Subject – A bit of detail" ...
```

These will generate a page title that looks like "Subject – A bit of detail" on the web.

## Limitations of GitHub Wikis and the features added by Wikiman

GitHub Wiki is a barebones documentation service that has stagnated since it diverged from the actively-developed [Gollum] long ago. There are better documentation tools out there, but sometimes it is nice to have a quick-and-dirty documentation solution that lives under the same roof as your repo. It is especially helpful for teaching/tutorial/"awesome list" repos, where you can ensure that fledgling coders have access to everything straight from the GitHub repo, documentation included.

The problem with GitHub Wikis is that there is no simple way to structure your wiki in a tree format, with some pages being subpages of others. And even if you manage that, there is no simple way to generate tree or relative navigation in the sidebar/footer of your pages. **Wikiman** seeks to ease the pain of GitHub Wikis, enabling tree views of pages, tables of contents, and relative navigation. It also permits adding, renaming, moving, and removing pages. This functionality is supported from a command line interface (CLI) in addition to scripting in the native Python.

[Gollum]: https://github.com/gollum/gollum/wiki

## Cloning your wiki pages in order to use Wikiman

GitHub Wikis are generated from Markdown pages inside a Git repo. This repo can be cloned locally by copying the link in the sidebar of the wiki on the internet. Look for the message "Clone this wiki locally". For example, if your project repo is hosted at

```text
https://github.com/user-name/repo-name.git
```

then the GitHub wiki for that project is hosted at

```text
https://github.com/user-name/repo-name.wiki.git
                                       ^^^^
```

## Wiki project structure enforced by Wikiman

Because of the limitations of GitHub Wikis, and to keep development effort reasonably low, **Wikiman** achieves its functionality by enforcing a certain project structure. Your pages must be found inside a subfolder named `wiki` in your GitHub Wiki repo. The first page in your wiki must be `Home.md`, immediately inside the `wiki` folder. The name of `Home.md` is enforced by the GitHub Wiki service, so it cannot be named differently.

The first time you invoke **Wikiman** from the CLI (try `wikiman update`), a `wiki` folder will be created, and `Home.md` will be placed within it (if such a structure doesn't already exist). If you build your wiki only using **Wikiman** commands, the proper structure will be enforced automatically. If you are migrating an existing wiki to be managed by **Wikiman**, then you will have to groom the pages into the expected format before continuing to manage it with **Wikiman**.

The expected folder structure of your GitHub Wiki repo is evident in the following example with random page names

```text
repo-name.wiki
│
... (other files and folders in the repo)
│
└───wiki
    │   Home.md
    │
    ├───00_Impeach-Vermilion-Vacuum
    │   │   Impeach-Vermilion-Vacuum.md
    │   │
    │   ├───00_Measure-Transient-Respite
    │   │       Measure-Transient-Respite.md
    │   │
    │   ├───01_Official-Union-Advantage
    │   │   │   Official-Union-Advantage.md
    │   │   │
    │   │   ├───00_Close-Waste-Transform
    │   │   │       Close-Waste-Transform.md
    │   │   │
    │   │   ├───01_Transit-Thrum-Middle
    │   │   │       Transit-Thrum-Middle.md
    │   │   │
    │   │   └───02_Serpentine-Hurry-Butcher
    │   │           Serpentine-Hurry-Butcher.md
    │   │
    │   └───02_Middle-Pasture-Floating
    │           Middle-Pasture-Floating.md
    │
    └───01_Equity-Substitute-Huddle
        │   Equity-Substitute-Huddle.md
        │
        ├───00_Automatic-Party-Merit
        │       Automatic-Party-Merit.md
        │
        └───01_Medium-Establish-Vital
                Medium-Establish-Vital.md
```

Similar functionality could be achieved by by storing the metadata of page relationships separately, and keeping the structure of the repo flat instead of nested. **Wikiman** enforces this tree structure, encoding page positions in folder titles, because it facilitates human navigation of the GitHub Wiki repo. The goal is to make building and modifying a GitHub Wiki less of a chore.

Invoking `wikiman update` generates sidebars and footers. Each page will have its own `_Footer.md` and `_Sidebar.md` generated next to it. These files contain the tree navigation, relative navigation, and table of contents created by **Wikiman**. Here is the same example wiki above, with some directories truncated by ellipses, after `wikiman update` has been performed

```text
repo-name.wiki
│
... (other files and folders in the repo)
│
└───wiki
    │   Home.md
    │   _Footer.md
    │   _Sidebar.md
    │
    ├───00_Impeach-Vermilion-Vacuum
    │   │   Impeach-Vermilion-Vacuum.md
    │   │   _Footer.md
    │   │   _Sidebar.md
    │   │
    │   ...
    │   │
    │   ├───01_Official-Union-Advantage
    │   │   │   Official-Union-Advantage.md
    │   │   │   _Footer.md
    │   │   │   _Sidebar.md
    │   │   │
    │   │   ...
    │   ...
    ...
```

## What comes next?

The CLI is in its near-final form, but the underlying Python logic will likely change over time. This repo will be contributed to by colleagues as a way of learning Python development practices, myself included. All of the functionality of **Wikiman** is in one module as of now. A group-development effort will be pursued as a way of learning the following things:

- Testing with pytest.
- Separating code into multiple modules.
- Refactoring functions that operate on "pages" (currently instances of `pathlib.Path`) into the methods and attributes of a custom `Page` class.
- Documentation of the API with Sphinx/ReadTheDocs.
- CI/CD workflows with GitHub Actions.
- Contributing via Pull Requests.
- Other development best-practices.

## Alternatives to Wikiman

The [github-wiki-sidebar] project is an `npm` package that generates a navigation menu in the sidebars of your GitHub Wiki pages. **Github-wiki-sidebar** puts the entire tree in the sidebar of each page. This is useful if you don't like the trees that **Wikiman** generates. **Wikiman** shows a tree view relative to the parent of a page, collapsing sections outside of the current one and not showing the entire tree all at once.

**Wikiman** is more ambitious than **github-wiki-sidebar** in that it enables page management, tables of contents, and relative navigation in the footers of pages. But sometimes you just need a static sidebar across all pages, and **github-wiki-sidebar** does an admirable job of that.

I suspect that any implementations that patch over the ugly parts of GitHub Wikis (**Wikiman** included) tend to be not very configurable. It is simply not worth it to make a fully-featured content manager for GitHub Wikis when the core service is so limited.

[github-wiki-sidebar]: https://github.com/adriantanasa/github-wiki-sidebar

## Alternatives to GitHub Wikis

GitHub Wikis are probably not suitable for large project documentation. While **Wikiman** seeks to ease the headaches of using GitHub Wikis, the service is functionally limited by the flat linking and support of only Markdown pages. Additionally, GitHub Wikis only support a subset of HTML, so if you have raw HTML in your pages, you may hit some insurmountable barriers. The following are documentation services that bring more to the table than GitHub Wikis:

- [Sphinx]: Great for Python projects. Less great (but still good) for non-Python projects.
- [MkDocs]: I haven't used this one personally, but it is a leading alternative to Sphinx.
- [Gollum]: Gollum supports reStructuredText in addition to Markdown, supports more HTML, and is all-around more feature-rich than GitHub Wikis. It is the project that GitHub Wikis diverged from ages ago.

Static site generators are less specific to code documentation, but they do tend to have a variety of docs-focused templates that lend a bit of style to your documentaion:

- [Hugo]: A feature-packed static site generator.
- [Jekyll]: The so-called "engine behind GitHub Pages". A static site generator in its own right.

GitHub Wikis handle docs generation and hosting for you. The alternatives just listed will generate your docs for you, but you still need to find a host. Hosting services for project documentation are numerous. Some of the big ones are as follows:

- [Read the Docs]: A behemoth for hosting Python docs, due to its coupling with the Python-focused Sphinx. Easily hooks into GitHub repos. Lots of helper features, like versioning your docs. Somewhat limiting in terms of styling.
- [GitHub Pages]: Not to be confused with GitHub Wikis. Pages are a free host for project documentation in Public repos. It is a bit less feature-rich than ReadTheDocs, but is a more generalized host.
- [GitBook]: I actually don't know much about this one.
- Any other host: Any host will do if you have static pages. The specialized hosts above just support more docs-focused things out-of-the-box.

[Sphinx]: https://www.sphinx-doc.org/en/master/
[MkDocs]: https://www.mkdocs.org/
[Gollum]: https://github.com/gollum/gollum/wiki

[Hugo]: https://gohugo.io/
[Jekyll]: https://jekyllrb.com/

[Read the Docs]: https://readthedocs.org/
[GitHub Pages]: https://pages.github.com/
[GitBook]: https://www.gitbook.com/

In my opinion, you should descend this list as the complexity of your project increases. Ideally you know the end-state complexity of your project from the outset, but sometimes it is unknown. Overambitious docs choices can be sluggish for quick projects, or for projects that aren't development-focused like teaching/tutorial/"awesome lists" on GitHub.

1. A `README.md` or `README.rst` in the root of your repo.
2. GitHub Wiki accompanied by **Wikiman**.
3. A combination of docs generator/host.
   1. Sphinx/ReadTheDocs for Python projects.
   2. GitHub Pages/Hugo in general.
   3. Other similar combos.
