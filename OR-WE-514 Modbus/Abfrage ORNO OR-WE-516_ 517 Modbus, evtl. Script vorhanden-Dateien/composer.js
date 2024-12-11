"use strict";define("composer",["taskbar","translator","composer/controls","composer/uploads","composer/formatting","composer/drafts","composer/tags","composer/categoryList","composer/preview","composer/resize","composer/autocomplete","scrollStop","topicThumbs","api"],function(t,e,i,o,n,a,r,s,d,c,p,l,u,f){var m={active:undefined,posts:{},bsEnvironment:undefined,formatting:undefined};$(window).off("resize",v).on("resize",v);$(document).off("keyup",h).on("keyup",h);v();$(window).on("action:composer.topics.post",function(t,e){localStorage.removeItem("category:"+e.data.cid+":bookmark");localStorage.removeItem("category:"+e.data.cid+":bookmark:clicked")});$(window).on("popstate",function(){var t=utils.findBootstrapEnvironment();if(m.active&&(t==="xs"||t==="sm")){if(!m.posts[m.active].modified){m.discard(m.active);if(m.discardConfirm&&m.discardConfirm.length){m.discardConfirm.modal("hide");delete m.discardConfirm}return}e.translate("[[modules:composer.discard]]",function(t){m.discardConfirm=bootbox.confirm(t,function(t){if(t){m.discard(m.active)}else{m.posts[m.active].modified=true}});m.posts[m.active].modified=false})}});function g(){var t=m.bsEnvironment;if(ajaxify.data.template.compose===true||t==="xs"||t==="sm"){history.back()}}function v(){var t=utils.findBootstrapEnvironment();var e=t==="xs"||t==="sm";if(d.toggle){if(d.env!==t&&e){d.env=t;d.toggle(false)}d.env=t}if(m.active!==undefined){c.reposition($('.composer[data-uuid="'+m.active+'"]'));if(!e&&window.location.pathname.startsWith(config.relative_path+"/compose")){history.back()}else if(e&&!window.location.pathname.startsWith(config.relative_path+"/compose")){E()}}m.bsEnvironment=t}function h(t){if(m.active){var e=t.which?t.which:t.keyCode;if(e===27){m.minimize(m.active)}}}function b(t){var e;var i;if(t.hasOwnProperty("cid")){e="cid"}else if(t.hasOwnProperty("tid")){e="tid"}else if(t.hasOwnProperty("pid")){e="pid"}i=t[e];for(var o in m.posts){if(m.posts[o].hasOwnProperty(e)&&i===m.posts[o][e]){return o}}return false}function y(i){var o=utils.generateUUID();var n=b(i);if(n){t.updateActive(n);return m.load(n)}var a="[[topic:composer.new_topic]]";if(i.action==="posts.reply"){a="[[topic:composer.replying_to]]"}else if(i.action==="posts.edit"){a="[[topic:composer.editing]]"}e.translate(a,function(e){t.push("composer",o,{title:e.replace("%1",'"'+i.title+'"')})});if(i.hasOwnProperty("cid")){i.save_id=["composer",app.user.uid,"cid",i.cid].join(":")}else if(i.hasOwnProperty("tid")){i.save_id=["composer",app.user.uid,"tid",i.tid].join(":")}else if(i.hasOwnProperty("pid")){i.save_id=["composer",app.user.uid,"pid",i.pid].join(":")}m.posts[o]=i;m.load(o)}function w(t,e){$('.composer[data-uuid="'+t+'"]').find(".composer-submit").removeAttr("disabled");app.alert({type:"danger",timeout:3e3,title:"",message:e,alert_id:"post_error"})}m.findByTid=function(t){for(var e in m.posts){if(m.posts.hasOwnProperty(e)&&m.posts[e].hasOwnProperty("tid")&&parseInt(m.posts[e].tid,10)===parseInt(t,10)){return e}}return null};m.addButton=function(t,e,i){n.addButton(t,e,i)};m.newTopic=function(t){var e={action:"topics.post",cid:t.cid,title:t.title||"",body:t.body||"",tags:t.tags||[],modified:!!(t.title&&t.title.length||t.body&&t.body.length),isMain:true};$(window).trigger("filter:composer.topic.push",{data:t,pushData:e});y(e)};m.addQuote=function(t,i,o,n,a,r,s){s=s||m.active;var c=(n||"").replace(/([\\`*_{}\[\]()#+\-.!])/g,"\\$1").replace(/\[/g,"&#91;").replace(/\]/g,"&#93;").replace(/%/g,"&#37;").replace(/,/g,"&#44;");if(r){r="> "+r.replace(/\n/g,"\n> ")+"\n\n"}var p="["+c+"]("+config.relative_path+"/post/"+(o||i)+")";if(s===undefined){if(n&&(o||i)){m.newReply(t,i,n,"[[modules:composer.user_said_in, "+a+", "+p+"]]\n"+r)}else{m.newReply(t,i,n,"[[modules:composer.user_said, "+a+"]]\n"+r)}return}else if(s!==m.active){m.load(s)}var l=$('.composer[data-uuid="'+s+'"]');var u=l.find("textarea");var f=u.val();if(n&&(o||i)){e.translate("[[modules:composer.user_said_in, "+a+", "+p+"]]\n",config.userLang||config.defaultLang,g)}else{e.translate("[[modules:composer.user_said, "+a+"]]\n",config.userLang||config.defaultLang,g)}function g(t){m.posts[s].body=(f.length?f+"\n\n":"")+t+r;u.val(m.posts[s].body);k(l);d.render(l)}};m.newReply=function(t,i,o,n){e.translate(n,config.userLang||config.defaultLang,function(e){y({action:"posts.reply",tid:t,toPid:i,title:o,body:e,modified:!!(o&&o.length||e&&e.length),isMain:false})})};m.editPost=function(t){socket.emit("plugins.composer.push",t,function(e,i){if(e){return app.alertError(e.message)}i.action="posts.edit";i.pid=t;i.modified=false;y(i)})};m.load=function(t){var e=$('.composer[data-uuid="'+t+'"]');if(e.length){L(t);c.reposition(e);k(e);C()}else if(m.formatting){x(t)}else{socket.emit("plugins.composer.getFormattingOptions",function(e,i){if(e){return app.alertError(e)}m.formatting=i;x(t)})}};m.enhance=function(t,i,c){if(!i&&!c){i=utils.generateUUID();m.posts[i]=ajaxify.data;c=ajaxify.data;t.attr("data-uuid",i)}var l=t.find("input.title");var u=t.find("input.handle");var f=t.find("input.tags");var v=t.find("textarea");var h=t.find(".composer-submit");s.init(t,m.posts[i]);n.addHandler(t);n.addComposerButtons();d.handleToggler(t);o.initialize(i);r.init(t,m.posts[i]);p.init(t,i);t.on("change","input, textarea",function(){m.posts[i].modified=true;a.updateVisibility("available",m.posts[i].save_id,true);a.updateVisibility("open",m.posts[i].save_id,true)});h.on("click",function(t){t.preventDefault();t.stopPropagation();$(this).attr("disabled",true);T(i)});require(["mousetrap"],function(e){e(t.get(0)).bind("mod+enter",function(){h.attr("disabled",true);T(i)})});t.find(".composer-discard").on("click",function(t){t.preventDefault();if(!m.posts[i].modified){m.discard(i);return g()}if(screenfull.isEnabled&&screenfull.isFullscreen){screenfull.exit()}var o=$(this).prop("disabled",true);e.translate("[[modules:composer.discard]]",function(t){bootbox.confirm(t,function(t){if(t){m.discard(i);g()}o.prop("disabled",false)})})});t.find(".composer-minimize, .minimize .trigger").on("click",function(t){t.preventDefault();t.stopPropagation();m.minimize(i)});v.on("input propertychange",function(){d.render(t)});v.on("scroll",function(){d.matchScroll(t)});d.render(t,function(){d.matchScroll(t)});a.init(t,c);var b=a.get(c.save_id);if(b&&b.title){l.val(b.title)}if(b&&b.handle){u.val(b.handle)}if(b&&b.tags){const t=b.tags.split(",");t.forEach(function(t){f.tagsinput("add",t)})}v.val(b.text?b.text:c.body);_(t);P(t);k(t);if(c.action==="posts.edit"){m.updateThumbCount(i,t)}if(!screenfull.isEnabled){$('[data-format="zen"]').addClass("hidden")}$(window).trigger("action:composer.enhanced",{postContainer:t,postData:c,draft:b})};function x(i){var o=m.posts[i];var n=o?o.hasOwnProperty("cid"):false;var a=o?!!o.isMain:false;var r=o?!!o.pid:false;var s=o?parseInt(o.uid,10)===0:false;var d=o.title.replace(/%/g,"&#37;").replace(/,/g,"&#44;");var p={title:d,mobile:m.bsEnvironment==="xs"||m.bsEnvironment==="sm",resizable:true,thumb:o.thumb,isTopicOrMain:n||a,minimumTagLength:config.minimumTagLength,maximumTagLength:config.maximumTagLength,isTopic:n,isEditing:r,showHandleInput:config.allowGuestHandles&&(app.user.uid===0||r&&s&&app.user.isAdmin),handle:o?o.handle||"":undefined,formatting:m.formatting,tagWhitelist:ajaxify.data.tagWhitelist,privileges:app.user.privileges};if(p.mobile){E();app.toggleNavbar(false)}o.mobile=m.bsEnvironment==="xs"||m.bsEnvironment==="sm";$(window).trigger("filter:composer.create",{postData:o,createData:p});app.parseAndTranslate("composer",p,function(n){if($('.composer.composer[data-uuid="'+i+'"]').length){return}n=$(n);n.find(".title").each(function(){$(this).text(e.unescape($(this).text()))});n.attr("data-uuid",i);$(document.body).append(n);var a=$(n[0]);c.reposition(a);m.enhance(a,i,o);L(i);a.on("click",function(){if(!t.isActive(i)){t.updateActive(i)}});c.handleResize(a);if(m.bsEnvironment==="xs"||m.bsEnvironment==="sm"){var r=a.find(".composer-submit");var s=a.find(".mobile-navbar .composer-submit");var d=a.find(".write");var p=d.attr("tabindex");r.removeAttr("tabindex");s.attr("tabindex",parseInt(p,10)+1);$(".category-name-container").on("click",function(){$(".category-selector").toggleClass("open")})}$(window).trigger("action:composer.loaded",{post_uuid:i,composerData:m.posts[i],formatting:m.formatting});l.apply(a.find(".write"));k(a);C()})}function E(){var t="compose?p="+window.location.pathname;var e=window.location.pathname.slice(1);if(e.startsWith(config.relative_path.slice(1))){e=e.slice(config.relative_path.length)}window.history.replaceState({url:null,returnPath:e},e,config.relative_path+"/"+e);window.history.pushState({url:t},t,config.relative_path+"/"+t)}function _(t){var e=t.find(".help");socket.emit("plugins.composer.renderHelp",function(t,i){if(!t&&i&&i.length>0){e.removeClass("hidden");e.on("click",function(){bootbox.alert(i)})}})}function P(t){var e=t.attr("data-uuid");var i=m.posts[e]&&m.posts[e].action==="posts.edit";var o=utils.findBootstrapEnvironment();var n=o==="xs"||o==="sm";if(i||n){return}app.enableTopicSearch({searchElements:{inputEl:t.find("input.title"),resultEl:t.find(".quick-search-container")},hideOnNoMatches:true})}function L(t){if(m.active&&m.active!==t){m.minimize(m.active)}m.active=t;$(window).trigger("action:composer.activate",{post_uuid:t})}function k(t){setTimeout(function(){var e=t.find("input.title");if(e.length){e.focus()}else{t.find("textarea").focus().putCursorAtEnd()}},20)}function T(t){var e=m.posts[t];var i=$('.composer[data-uuid="'+t+'"]');var n=i.find(".handle");var d=i.find(".title");var c=i.find("textarea");var p=i.find("input#topic-thumb-url");var l=e.hasOwnProperty("template")&&e.template.compose===true;const u=i.find(".composer-submit");d.val(d.val().trim());c.val(utils.rtrim(c.val()));if(p.length){p.val(p.val().trim())}var v=e.action;var h=(e.hasOwnProperty("cid")||parseInt(e.pid,10))&&i.find("input.title").length;var b=!h||h&&parseInt(e.cid,10);var y={post_uuid:t,postData:e,postContainer:i,titleEl:d,titleLen:d.val().length,bodyEl:c,bodyLen:c.val().length};$(window).trigger("action:composer.check",y);if(o.inProgress[t]&&o.inProgress[t].length){return w(t,"[[error:still-uploading]]")}else if(h&&y.titleLen<parseInt(config.minimumTitleLength,10)){return w(t,"[[error:title-too-short, "+config.minimumTitleLength+"]]")}else if(h&&y.titleLen>parseInt(config.maximumTitleLength,10)){return w(t,"[[error:title-too-long, "+config.maximumTitleLength+"]]")}else if(v==="topics.post"&&!b){return w(t,"[[error:category-not-selected]]")}else if(y.bodyLen<parseInt(config.minimumPostLength,10)){return w(t,"[[error:content-too-short, "+config.minimumPostLength+"]]")}else if(y.bodyLen>parseInt(config.maximumPostLength,10)){return w(t,"[[error:content-too-long, "+config.maximumPostLength+"]]")}else if(h&&!r.isEnoughTags(t)){return w(t,"[[error:not-enough-tags, "+r.minTagCount()+"]]")}let x={uuid:t};let E="post";let _="";if(v==="topics.post"){_="/topics";x={...x,handle:n?n.val():undefined,title:d.val(),content:c.val(),thumb:p.val()||"",cid:s.getSelectedCid(),tags:r.getTags(t)}}else if(v==="posts.reply"){_=`/topics/${e.tid}`;x={...x,tid:e.tid,handle:n?n.val():undefined,content:c.val(),toPid:e.toPid}}else if(v==="posts.edit"){E="put";_=`/posts/${e.pid}`;x={...x,pid:e.pid,handle:n?n.val():undefined,content:c.val(),title:d.val(),thumb:p.val()||"",tags:r.getTags(t)}}var P={composerEl:i,action:v,composerData:x,postData:e,redirect:true};$(window).trigger("action:composer.submit",P);var L=$('#taskbar .composer[data-uuid="'+t+'"] i');var k=i.find(".write");L.removeClass("fa-plus").addClass("fa-circle-o-notch fa-spin");m.minimize(t);k.prop("readonly",true);f[E](_,x).then(o=>{i.find(".composer-submit").removeAttr("disabled");e.submitted=true;m.discard(t);a.removeDraft(e.save_id);if(o.queued){bootbox.alert(o.message)}else if(v==="topics.post"){if(P.redirect){ajaxify.go("topic/"+o.slug,undefined,l||m.bsEnvironment==="xs"||m.bsEnvironment==="sm")}}else if(v==="posts.reply"){if(l||m.bsEnvironment==="xs"||m.bsEnvironment==="sm"){window.history.back()}else if(P.redirect&&(ajaxify.data.template.name!=="topic"||ajaxify.data.template.topic&&parseInt(e.tid,10)!==parseInt(ajaxify.data.tid,10))){ajaxify.go("post/"+o.pid)}}else{g()}$(window).trigger("action:composer."+v,{composerData:x,data:o})}).catch(e=>{m.load(t);k.prop("readonly",false);u.prop("disabled",false);if(e.message==="[[error:email-not-confirmed]]"){return app.showEmailConfirmWarning(e)}app.alertError(e)})}function C(){$("html").addClass("composing")}function D(){$("body").css({paddingBottom:0});$("html").removeClass("composing");app.toggleNavbar(true)}m.discard=function(e){if(m.posts[e]){var i=m.posts[e];var o=$('.composer[data-uuid="'+e+'"]');o.remove();a.removeDraft(i.save_id);u.deleteAll(e);t.discard("composer",e);$('[data-action="post"]').removeAttr("disabled");$(window).trigger("action:composer.discard",{post_uuid:e,postData:i});delete m.posts[e];m.active=undefined}D()};m.close=m.discard;m.minimize=function(e){var i=$('.composer[data-uuid="'+e+'"]');i.css("visibility","hidden");m.active=undefined;t.minimize("composer",e);$(window).trigger("action:composer.minimize",{post_uuid:e});D()};m.updateThumbCount=function(t,e){const i=m.posts[t];if(i.action==="topics.post"||i.action==="posts.edit"&&i.isMain){const o=[u.get(t)];if(i.pid){o.push(u.getByPid(i.pid))}Promise.all(o).then(t=>{t=t.reduce((t,e)=>{t=t.concat(e);return t});if(t.length){const i=e.find('[data-format="thumbs"]');i.attr("data-count",t.length)}})}};return m});
//# sourceMappingURL=composer.js.map