<!DOCTYPE html>

<title>Fickileaks — Beziehungen anschauen</title>

<link rel="stylesheet" href="/css/reset.css"/>
<link rel="stylesheet" href="/css/lib/jquery-ui/jquery-ui-1.8.12.custom.css"/>

<script src="/js/lib/jquery-1.5.2.min.js"></script>
<script src="/js/lib/%24.include.js"></script>

<script>
    $.include(
        '/js/relationview.js',
        /* dependencies: node and graph types */
        [
            $.include(
                '/js/nodes.js',
                [
                    $.include('/js/lib/jit.js')
                ]
            ),
            $.include('/js/edges.js')
        ]
    );
</script>

<script src="/js/lib/jquery-ui-1.8.12.custom.min.js"></script>
<script src=""></script>

<script src="/js/lib/modernizr-1.7.min.js"></script>
<script src="/js/lib/js-webshim/minified/polyfiller.js"></script>
<script>$.webshims.polyfill('details');</script>

<style>
html, body {
    line-height: 1.5;
    height: 100%;
}

button {
    box-sizing: border-box;
    line-height: 16px;
    padding: 5px;
    width: 100%;
}

button > img {
    vertical-align: text-bottom;
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

#filters {
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

<section id="filters">
    <h1>Quellen</h1>
    <form>
        <input type="email" class="autocomplete">
    </form>
    <button id="add">
        <img src="/img/icons/list-add.png" alt="+">
        Hinzufügen
    </button>
    <ul id="querylist"></ul>
    <script>
        var inputField = $('input[type=email].autocomplete');
        inputField.autocomplete({
            source: "/users/autocomplete"
            /*minLength: 2*/
            });

        $('#add').click(function() {
            var value = inputField.val();

            $('#querylist > li').each(function(index) {
                /* empty input field if value has already been added */
                if ($(this).text() == value) {
                    inputField.val('');
                }
            });

            /* add value if it is not empty */
            if (inputField.val() != '') {
                $('#querylist').append($('<li>' + value + '</li>'));
                inputField.val('');

                /* build query */
                var query = {
                    users: []
                }
                $('#querylist > li').each(function(index) {
                    query['users'].push($(this).text());
                });
                $.get('/relations/infovis', query, function(json){
                    console.log(json);
                });
            }
        });
    </script>
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
