(function(f,l,j){if(!$.webshims){var p=[navigator.browserLanguage||navigator.language||"",$("html").attr("lang")||""];$.webshims={addReady:function(b){$(function(){b(j,$([]))})},ready:function(b,h){h()},activeLang:function(){return p}}}var d=$.webshims,e={},c=$.attr,a=false,g,i,r=function(b){d.refreshCustomValidityRules(b.target)};d.customErrorMessages={};d.addCustomValidityRule=function(b,h,k){e[b]=h;if(!d.customErrorMessages[b]){d.customErrorMessages[b]=[];d.customErrorMessages[b][""]=k||b}$.isReady&&
a&&$("input, select, textarea").each(function(){q(this)})};d.refreshCustomValidityRules=function(b){if(!(!b.form||!i&&!$.attr(b,"willValidate"))){g=true;var h=$.data(b,"customMismatchedRule"),k=c(b,"validity")||{},m="";if(h||!k.customError){var s=$(b).val();$.each(e,function(o,t){m=t(b,s)||"";h=o;if(m){if(typeof m!="string")m=b.getAttribute("x-moz-errormessage")||b.getAttribute("data-errormessage")||d.customErrorMessages[o][d.activeLang()[0]]||d.customErrorMessages[o][d.activeLang()[1]]||d.customErrorMessages[o][""];
return false}});m&&$.data(b,"customMismatchedRule",h);$(b).setCustomValidity(m)}g=false}};var q=d.refreshCustomValidityRules;d.ready("forms",function(){a=true;c=$.attr;$.attr=function(h,k){k=="validity"&&!g&&q(h);return c.apply(this,arguments)};var b=$.fn.setCustomValidity||function(h){return this.each(function(){this.setCustomValidity&&this.setCustomValidity(h)})};$.fn.setCustomValidity=function(){g||this.data("customMismatchedRule","");return b.apply(this,arguments)};j.addEventListener&&j.createElement("form").checkValidity&&
j.addEventListener("change",r,true);d.addReady(function(h,k){i=true;$("input, select, textarea",h).add(k.filter("input, select, textarea")).each(function(){q(this)});i=false});$(j).bind("refreshCustomValidityRules",r)})})(jQuery,window,document);
(function(f,l,j){l=f.webshims.addCustomValidityRule;l("partialPattern",function(e,c){if(c&&e.getAttribute("data-partial-pattern")){var a=f(e).data("partial-pattern");if(a)return!RegExp("("+a+")","i").test(c)}},"This format is not allowed here.");l("tooShort",function(e,c){if(c&&e.getAttribute("data-minlength"))return f(e).data("minlength")>c.length},"Entered value is too short.");var p=/[^0-9-]+/;l("creditcard",function(e,c){if(c&&f(e).hasClass("creditcard-input")){if(!p.test(c))return true;var a=
0,g=0,i=false;c=c.replace(/\D/g,"");for(n=c.length-1;n>=0;n--){g=c.charAt(n);g=parseInt(g,10);if(i&&(g*=2)>9)g-=9;a+=g;i=!i}return a%10!==0}},"Please enter a valid credit card number");var d={prop:"value","from-prop":"value",toggle:false};l("dependent",function(e,c){if(e.getAttribute("data-dependent-validation")){var a=f(e).data("dependent-validation");if(a){var g=function(){var i=f.attr(a.masterElement,a["from-prop"]);if(a.toggle)i=!i;f.attr(e,a.prop,i)};if(!a._init||!a.masterElement){if(typeof a==
"string")a={from:a};a.masterElement=j.getElementById(a.from)||j.getElementsByName(a.from||[])[0];if(!a.masterElement||!a.masterElement.form)return;if(/radio|checkbox/i.test(a.masterElement.type)){a["from-prop"]||(a["from-prop"]="checked");if(!a.prop&&a["from-prop"]=="checked")a.prop="disabled"}a=f.data(e,"dependent-validation",f.extend({_init:true},d,a));a.prop!=="value"?f(a.masterElement).bind("change",g):f(a.masterElement).bind("change",function(){f.webshims.refreshCustomValidityRules(e)})}if(a.prop==
"value")return f.attr(a.masterElement,"value")!=c;else{g();return""}}}},"The value of this field does not repeat the value of the other field")})(jQuery,window,document);
