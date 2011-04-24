<!DOCTYPE html>

<title>Fickileaks — Beziehungen anschauen</title>

<link rel="stylesheet" href="/css/reset.css"/>

<script src="/js/lib/jquery-1.5.2.min.js"></script>
<script src="/js/lib/jit.js"></script>

<script src="/js/lib/modernizr-1.7.min.js"></script>
<script src="/js/lib/js-webshim/minified/polyfiller.js"></script>
<script>$.webshims.polyfill('details');</script>

<style>
html, body {
    line-height: 1.5;
    height: 100%;
}

ul {
    list-style-position: inside;
    margin-left: 10px;
}

body > header,
body > section,
.tip {
    background-color: white;
    border: 1px solid #2e3436;
    color: black;
    display: block;
    margin: 10px;
    max-width: 200px;
    padding: 10px;
    z-index: 1;
}

body > header > h1 {
    font-size: 2em;
}

body > section > h1 {
    font-size: 1.5em;
}

body > section > section > h1 {
    font-size: 1.25em;
}

#header {
    top: 10px;
    left: 10px;
    position: absolute;
}

#queryform {
    display: inline-block;
    right: 10px;
    top: 10px;
    position: absolute;
}

#legend {
    bottom: 10px;
    left: 10px;
    position: absolute;
}

    #legend > ul {
        list-style-type: none;
        margin: 0;
    }

    #legend .grope {
        background-color: white;
        color: #ef2929;
    }

    #legend .kiss {
        background-color: white;
        color: #fcaf3e;
    }

    #legend .fuck {
        background-color: white;
        color: #fce94f;
    }

    #legend .oral {
        background-color: white;
        color: #8ae234;
    }

    #legend .anal {
        background-color: white;
        color: #729fcf;
    }

    #legend .sm {
        background-color: white;
        color: #ad7fa8;
    }

#nodeinfo {
    bottom: 10px;
    right: 10px;
    position: absolute;
}

#nodeinfo > details > ul {
    list-style-type: none;
}

#graph {
    background-color: #f2f8ff;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
}

#graph,
#graph * {
    z-index: 0 !important;
}
</style>

<script>
function addInput() {
    $()
}
</script>

<header id="header">
    <h1>Fickileaks</h1>
    <h2>Beziehungen anschauen</h2>
</header>

<section id="queryform">
    <h1>Filterung</h1>
    <form>
        <input type=text/>
        <button onclick="addInput(this)">+</button>
    </form>
</section>

<section id="legend">
    <h1>Legende</h1>
    <ul>
        <li><span class="grope">█</span> Fummeln
        <li><span class="kiss">█</span> Küssen
        <li><span class="fuck">█</span> Vaginalsex
        <li><span class="oral">█</span> Oralsex
        <li><span class="anal">█</span> Analsex
        <li><span class="sm">█</span> SM-Spielchen
    </ul>
</section>

<section id="nodeinfo">
    <h1 id="nodename">Klicke einen Knoten!</h1>
    <details>
        <summary>
            Namen
            (<span id="namecount"></span>)
        </summary>
        <ul id="namelist"></ul>
    </details>
    <details>
        <summary>
            <abbr title="Uniform Resource Locator">URL</abbr>s
            (<span id="urlcount"></span>)
        </summary>
        <ul id="urllist"></ul>
    </details>
    <details>
        <summary>
            Kontakte
            (<span id="relationcount"></span>)
        </summary>
        <ul id="relationlist"></ul>
    </details>
    <p>
        Klicke auf die Dreiecke, um zu erfahren, wer etwas behauptet hat.
    </p>
</section>

<div id=graph></div>

<script src="/js/relationview.js"></script>
