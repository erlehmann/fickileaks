(function(e){if(!Modernizr.genericDOM){var i=e.webshims,u=document,r,n,s=/<([\w:]+)/,t={option:1,optgroup:1,legend:1,thead:1,tr:1,td:1,col:1,area:1},m=/^(?:[^<]*(<[\w\W]+>)[^>]*$)/;i.fixHTML5=function(o){if(typeof o!="string"||t[(s.exec(o)||["",""])[1].toLowerCase()])return o;if(!n){r=u.body;if(!r)return o;n=u.createElement("div");n.style.display="none"}var l=n.cloneNode(false);r.appendChild(l);l.innerHTML=o;r.removeChild(l);return l.childNodes};if(i.fn&&i.fn.init){var p=i.fn.init;i.fn.init=function(o){if(o&&
m.exec(o))arguments[0]=i.fixHTML5(o);return p.apply(this,arguments)};i.fn.init.prototype=p.prototype}}})(jQuery);
jQuery.webshims.register("dom-extend",function(e,i,u,r,n){var s=i.modules,t=e.attr,m={},p={};e.attr=function(c,b,a,d,f){var h=(c.nodeName||"").toLowerCase();if(!h||c.nodeType!==1)return t(c,b,a,d,f);var g=m[h],k;if(g)g=g[b];if(!g)if(g=m["*"])g=g[b];if(g)if(a===n)return g.get?g.get.call(c):g.value;else{if(g.set)k=g.set.call(c,a)}else k=t(c,b,a,d,f);a!==n&&p[h]&&p[h][b]&&e.each(p[h][b],function(j,q){q.call(c,a)});return k};var o=function(c,b,a){m[c]||(m[c]={});var d=m[c][b],f=function(h,g,k){if(g&&
g[h])return g[h];if(k&&k[h])return k[h];return function(j){return t(this,b,j)}};m[c][b]=a;if(a.value===n){if(!a.set)a.set=a.writeable?f("set",a,d):i.cfg.useStrict?function(){throw b+" is readonly on "+c;}:e.noop;if(!a.get)a.get=f("get",a,d)}e.each(["value","get","set"],function(h,g){if(a[g])a["_sup"+g]=f(g,d)})},l=function(){var c={};i.addReady(function(f,h){var g={},k=function(j){if(!g[j]){g[j]=e(f.getElementsByTagName(j));if(h[0]&&e.nodeName(h[0],j))g[j]=g[j].add(h)}};e.each(c,function(j,q){k(j);
!q||!q.forEach?i.warn("Error: with "+j+"-property. methods: "+q):q.forEach(function(v){g[j].each(v)})});g=null});var b,a=e([]),d=function(f,h){if(c[f])c[f].push(h);else c[f]=[h];if(e.isDOMReady)(b||e(r.getElementsByTagName(f))).each(h)};return{createTmpCache:function(f){if(e.isDOMReady)b=b||e(r.getElementsByTagName(f));return b||a},flushTmpCache:function(){b=null},content:function(f,h){d(f,function(){e(this).filter("["+h+"]").attr(h,function(g,k){return k})})},createElement:function(f,h){d(f,h)},
extendValue:function(f,h,g){d(f,function(){e(this).each(function(){(e.data(this,"_oldPolyfilledValue")||e.data(this,"_oldPolyfilledValue",{}))[h]=this[h];this[h]=g})})}}}(),w=function(){var c=i.getPrototypeOf(r.createElement("foobar")),b=Object.prototype.hasOwnProperty;return function(a,d,f){var h=r.createElement(a),g=i.getPrototypeOf(h);if(g&&c!==g&&(!h[d]||!b.call(h,d))){var k=h[d];f._supvalue=function(){if(k&&k.apply)return k.apply(this,arguments);return k};g[d]=f.value}else{f._supvalue=function(){var j=
e.data(this,"_oldPolyfilledValue");if(j&&j[d]&&j[d].apply)return j[d].apply(this,arguments);return j&&j[d]};l.extendValue(a,d,f.value)}f.value._supvalue=f._supvalue}}();e.extend(i,{getID:function(){var c=(new Date).getTime();return function(b){b=e(b);var a=b.attr("id");if(!a){c++;a="elem-id-"+c;b.attr("id",a)}return a}}(),defineNodeNameProperty:function(c,b,a){a=e.extend({writeable:true,idl:true},a);if(a.isBoolean){var d=a.set;a.set=function(f){f=!!f;i.contentAttr(this,b,f);d&&d.call(this,f);return f};
a.get=a.get||function(){return i.contentAttr(this,b)!=null}}o(c,b,a);c!="*"&&i.cfg.extendNative&&a.value&&e.isFunction(a.value)&&w(c,b,a);a.initAttr&&l.content(c,b);return a},defineNodeNameProperties:function(c,b,a){for(var d in b){!a&&b[d].initAttr&&l.createTmpCache(c);b[d]=i.defineNodeNameProperty(c,d,b[d])}a||l.flushTmpCache();return b},createElement:function(c,b,a){var d;if(e.isFunction(b))b={after:b};l.createTmpCache(c);b.before&&l.createElement(c,b.before);if(a)d=i.defineNodeNameProperties(c,
a,true);b.after&&l.createElement(c,b.after);l.flushTmpCache();return d},onNodeNamesPropertyModify:function(c,b,a){if(typeof c=="string")c=c.split(/\s*,\s*/);if(e.isFunction(a))a={set:a};c.forEach(function(d){p[d]||(p[d]={});p[d][b]||(p[d][b]=[]);a.set&&p[d][b].push(a.set);a.initAttr&&l.content(d,b)})},defineNodeNamesBooleanProperty:function(c,b,a){a=a||{};a.isBoolean=true;i.defineNodeNamesProperty(c,b,a)},contentAttr:function(c,b,a){if(c.nodeName){if(a===n){a=(c.attributes[b]||{}).value;return a==
null?n:a}if(typeof a=="boolean")a?c.setAttribute(b,b):c.removeAttribute(b);else c.setAttribute(b,a)}},activeLang:function(){var c=[navigator.browserLanguage||navigator.language||""],b=e("html").attr("lang");b&&c.push(b);return function(a,d,f,h){if(a)if(!d||!f){if(a!==c[0]){c[0]=a;e(r).triggerHandler("webshimLocalizationReady",c)}}else{var g=(d=s[d].options)&&d.availabeLangs,k=function(q){if(e.inArray(q,g)!==-1){i.loader.loadScript(d.langSrc+q+".js",function(){a[q]?f(a[q]):e(function(){a[q]&&f(a[q])})});
return true}return false},j;e.each(c,function(q,v){var x=v.split("-")[0];if(a[v]||a[x]){j=true;f(a[v]||a[x]);return false}if(g&&d.langSrc&&(k(v)||k(x))){j=true;return false}});!j&&h&&h()}return c}}()});e.each({defineNodeNamesProperty:"defineNodeNameProperty",defineNodeNamesProperties:"defineNodeNameProperties",createElements:"createElement"},function(c,b){i[c]=function(a,d,f){if(typeof a=="string")a=a.split(/\s*,\s*/);var h={};a.forEach(function(g){h[g]=i[b](g,d,f)});return h}});i.isReady("webshimLocalization",
true)});
(function(e,i){var u=parseFloat(e.browser.version,10);if(e.browser.msie&&u<10&&u>7||e.browser.mozilla&&u<2||e.browser.webkit&&u<535){var r={article:"article",aside:"complementary",section:"region",nav:"navigation",address:"contentinfo"},n=function(s,t){s.getAttribute("role")||s.setAttribute("role",t)};e.webshims.addReady(function(s,t){e.each(r,function(l,w){for(var c=e(l,s).add(t.filter(l)),b=0,a=c.length;b<a;b++)n(c[b],w)});if(s===i){var m=i.getElementsByTagName("header")[0],p=i.getElementsByTagName("footer"),o=
p.length;m&&!e(m).closest("section, article")[0]&&n(m,"banner");if(o){m=p[o-1];e(m).closest("section, article")[0]||n(m,"contentinfo")}}})}})(jQuery,document);
