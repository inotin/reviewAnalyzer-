<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->





<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Review Analyzer</h3>

  <p align="center">
    A tool for a quantitative assessment of reviews of products inculding YouTube videos
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/inotin/reviewAnalyzer">View Demo</a>
    ·
    <a href="https://github.com/inotin/reviewAnalyzer/issues">Report Bug</a>
    ·
    <a href="https://github.com/inotin/reviewAnalyzer/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com). -->


Once upon a time I realized that if you want to get objective information about some product, you have to spend a vast amount of time reading and watching reviews to distill valuable facts. The tool that I am trying to implement provides quantative assessment for a feature of products.

What are the inputs?
* Set of URLs for a group of products
* Key words for the feature/features

That's it!
What will you get?
* The comparative quantified asessment of products by their feature/features

Of course, there's a lot to do to calibrate the model but even now I get the results pretty close to expected.

### To Do List
- [x] Make initial commit
- [x] Add comments to the functions
- [ ] Update README.md. The used template can be found here: [https://github.com/othneildrew/Best-README-Template](https://github.com/othneildrew/Best-README-Template)
- [x] Add support of text reviews
- [ ] Implement JSON input for key words, sets of URLs
- [ ] Implement JSON input for dictionaries of scores
- [ ] Implement automatic feature detection
- [ ] Implement automatic descriptive words detection

### Built With
This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [Laravel](https://laravel.com)



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* youtube_transcript_api
```sh
pip install youtube_transcript_api
pip install bs4
pip install nltk 
```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
```sh
git clone https://github.com/your_username_/Project-Name.git
```
3. Install NPM packages
```sh
npm install
```
4. Enter your API in `config.js`
```JS
const API_KEY = 'ENTER YOUR API';
```



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/inotin/reviewAnalyzer/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Ilia Notin - notin13@gmail.com

Project Link: [https://github.com/inotin/reviewAnalyzer](https://github.com/inotin/reviewAnalyzer)


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Template for README.md](https://github.com/othneildrew/Best-README-Template/graphs/contributors)






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/inotin/reviewAnalyzer.svg?style=flat-square
[contributors-url]: https://github.com/inotin/reviewAnalyzer/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/inotin/reviewAnalyzer.svg?style=flat-square
[forks-url]: https://github.com/inotin/reviewAnalyzer/network/members
[stars-shield]: https://img.shields.io/github/stars/inotin/reviewAnalyzer.svg?style=flat-square
[stars-url]: https://github.com/inotin/reviewAnalyzer/stargazers
[issues-shield]: https://img.shields.io/github/issues/inotin/reviewAnalyzer.svg?style=flat-square
[issues-url]: https://github.com/inotin/reviewAnalyzer/issues
[license-shield]: https://img.shields.io/github/license/inotin/reviewAnalyzer.svg?style=flat-square
[license-url]: https://github.com/inotin/reviewAnalyzer/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/inotin/
[product-screenshot]: images/screenshot.png
