"""
Mac based build commands
"""


# 3rd party
import invoke


@invoke.task
def copy_bepinex(ctx, version="5.4.21"):
    """
    copy from https://github.com/BepInEx/BepInEx/releases into Timberborn folder
    """
    ctx.run("rm -rf ~/Downloads/BepInEx")
    ctx.run("mkdir -p ~/Downloads/BepInEx")
    ctx.run(
        "wget "
        "https://github.com/BepInEx/BepInEx/releases/download"
        f"/v{version}/BepInEx_unix_{version}.0.zip "
        "-O ~/Downloads/BepInEx/BepInEx.zip"
    )
    ctx.run("unzip ~/Downloads/BepInEx/BepInEx.zip")
    ctx.run("rm ~/Downloads/BepInEx/BepInEx.zip")
    ctx.run(
        r"cp -rv "
        r"~/Downloads/BepInEx/* "
        r"~/Library/Application\ Support/Steam/steamapps/common/Timberborn/",
    )
