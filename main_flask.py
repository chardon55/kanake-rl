from flask import Flask, make_response, request

from pycefl.environment import ChessEnvironment
import rest_interface.chess.agent as interfaces

app = Flask(__name__)

env = ChessEnvironment()
agent = interfaces.init_latest_agent()


@app.route("/ping")
def ping():
    res = make_response('Pong!', 200)
    res.mimetype = "text/plain"
    return res


@app.route("/init")
def init_env():
    env.reset()


@app.route("/check")
def check():
    is_valid = interfaces.check_rule(
        env.chessboard.numpy_chessboard,
        interfaces.interpreter.parse(request.args.get('s'), (8, 8)),
        env
    )

    res = make_response("", 200 if is_valid else 409)
    res.mimetype = "text/plain"
    return res


@app.route("/step")
def step():
    s2 = interfaces.interpreter.parse(request.args.get('s'), (8, 8))

    is_valid = interfaces.check_rule(
        env.chessboard.numpy_chessboard, s2, env
    )

    if not is_valid:
        res = make_response("", 409)
        res.mimetype = "text/plain"
        return res

    env.update_state(s2)
    result = interfaces.interpret_action(
        agent.select_action(env.chessboard.cb, explore=False), env
    )

    return result


def main():
    app.run(port=9826, debug=True)


if __name__ == '__main__':
    main()
