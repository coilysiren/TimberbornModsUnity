# 3rd party
import invoke


@invoke.task
def copy_bepinex(ctx):
    ctx.run(
        r"cp -r ~/Downloads/BepInEx/* ~/Library/Application\ Support/Steam/steamapps/common/Timberborn/",
        pty=True,
        echo=True,
    )
