"use strict";
function sleep(s) {
  return new Promise((resolve) => setTimeout(resolve, s));
}

async function main() {
  globalThis.pyodide = await loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.18.0/full/",
  });
  let namespace = pyodide.globals.get("dict")();
  let currentQuestion = "'init'";

  const prompt = document.getElementById('program').textContent;
  document.getElementById('loader').remove();
  pyodide.runPython(
    `
import sys
import js
from pyodide import to_js
from pyodide.console import PyodideConsole, repr_shorten, BANNER
import __main__
BANNER = js.document.getElementById('ascii-title').textContent
BANNER = BANNER + """

                            Press RETURN to begin.
"""
js.pyconsole = PyodideConsole(__main__.__dict__)
async def await_fut(fut):
  return to_js([await fut]);
`,
    namespace
  );
  let repr_shorten = namespace.get("repr_shorten");
  let banner = namespace.get("BANNER");
  let await_fut = namespace.get("await_fut");
  namespace.destroy();

  let ps1 = "> ",
    ps2 = "... ";

  async function lock() {
    let resolve;
    let ready = term.ready;
    term.ready = new Promise((res) => (resolve = res));
    await ready;
    return resolve;
  }

  async function interpreter(response) {
    let unlock = await lock();
    term.pause();
    // multiline should be splitted (useful when pasting)
    const handler = `
${prompt}
handle_input(${currentQuestion}, '${response}')
`;
    for (const c of handler.split("\n")) {
      let fut = pyconsole.push(c);
      term.set_prompt(fut.syntax_check === "incomplete" ? ps2 : ps1);
      switch (fut.syntax_check) {
        case "syntax-error":
          term.error(fut.formatted_error.trimEnd());
          continue;
        case "incomplete":
          continue;
        case "complete":
          break;
        default:
          throw new Error(`Unexpected type ${ty}`);
      }
      // In Javascript, await automatically also awaits any results of
      // awaits, so if an async function returns a future, it will await
      // the inner future too. This is not what we want so we
      // temporarily put it into a list to protect it.
      let wrapped = await_fut(fut);
      // complete case, get result / error and print it.
      try {
        let [value] = await wrapped;
        if (value !== undefined) {
          currentQuestion = repr_shorten.callKwargs(value, {
            separator: "\\n[[;orange;]<long output truncated>]\\n",
          })
        }
        if (pyodide.isPyProxy(value)) {
          value.destroy();
        }
      } catch (e) {
        if (e.constructor.name === "PythonError") {
          term.error(fut.formatted_error.trimEnd());
        } else {
          throw e;
        }
      } finally {
        fut.destroy();
        wrapped.destroy();
      }
    }
    term.resume();
    await sleep(10);
    unlock();
  }

  let term = $("body").terminal(interpreter, {
    greetings: banner,
    prompt: ps1,
    completionEscape: false,
    completion: function (command, callback) {
      callback(pyconsole.complete(command).toJs()[0]);
    },
  });
  window.term = term;
  pyconsole.stdout_callback = (s) => term.echo(s, { newline: false });
  pyconsole.stderr_callback = (s) => {
    term.error(s.trimEnd());
  };
  term.ready = Promise.resolve();
  pyodide._module.on_fatal = async (e) => {
    term.error(
      "Pyodide has suffered a fatal error. Please report this to the Pyodide maintainers."
    );
    term.error("The cause of the fatal error was:");
    term.error(e);
    term.error("Look in the browser console for more details.");
    await term.ready;
    term.pause();
    await sleep(15);
    term.pause();
  };
}
window.console_ready = main();