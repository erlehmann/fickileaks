<!DOCTYPE html>

<title>relation view</title>

<link rel="stylesheet" href="/css/reset.css"/>

<script src="/js/lib/jquery-1.4.4.min.js"></script>
<script src="/js/lib/jit.js"></script>

<style>
html, body {
    line-height: 1.5;
    height: 100%;
}

#graph {
    background-color: #f2f8ff;
    height: 100%;
    width: 100%;
}

.tip {
    color: #2e3436;
    background-color: #eeeeec;
    border: 1px solid #2e3436;
    padding: 1em;
}

.tip ul {
    margin-left: 20px;
}

#legend {
    background-color: white;
    border: 2px solid black;
    border-radius: 1em;
    color: black;
    display: block;
    padding: 0.5em 1em;
    position: absolute;
    right: 1em;
    top: 1em;
}

    #legend > h1 {
        display: none;
    }

    #legend > ul {
        list-style-type: none;
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
</style>

<div id=graph></div>

<section id="legend">
    <h1>Legend</h1>
    <ul>
        <li><span class="grope">█</span> Fummeln</li>
        <li><span class="kiss">█</span> Küssen</li>
        <li><span class="fuck">█</span> Vaginalsex</li>
        <li><span class="oral">█</span> Oralsex</li>
        <li><span class="anal">█</span> Analsex</li>
        <li><span class="sm">█</span> SM-Spielchen</li>
    </ul>
</section>

<script src="/js/relationview.js"></script>
