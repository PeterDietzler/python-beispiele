
(function (factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else if (typeof define === 'function' && define.amd) {
    define(factory);
  }
})(function () {
  function compiled(helpers, context, guard, iter, helper) {
    var __escape = helpers.__escape;
    var value = context;
    return "<div class=\"cookie-consent\">\n    <button class=\"pull-right btn btn-primary\">" + 
      __escape(guard(context && context['dismiss'])) + 
      "</button>\n    " + 
      __escape(guard(context && context['message'])) + 
      " <a target=\"_blank\" rel=\"noopener\" href=\"" + 
      __escape(guard(context && context['link_url'])) + 
      "\">" + 
      __escape(guard(context && context['link'])) + 
      "</a>\n</div>\n";
  }

  compiled.blocks = {
    
  };

  return compiled;
})
