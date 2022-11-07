"""
Mac based build commands
"""

# builtin
import copy
import enum


# 3rd party
import invoke


class VARS(enum.Enum):
    BEPINEX_VERSION = "5.4.21"
    TIMBERAPI_VERSION = "0.5.0.0"
    STEAMAPP = r"~/Library/Application\ Support/Steam/steamapps/common/Timberborn/"


@invoke.task
def setup_bepinex(ctx):
    """
    setup https://github.com/BepInEx/BepInEx/releases in the Timberborn folder
    """

    ####################
    # download BepInEx #
    ####################

    ctx.run("rm -rf .downloads/BepInEx")
    ctx.run("mkdir -p .downloads/BepInEx")
    ctx.run(
        "wget "
        "https://github.com/BepInEx/BepInEx/releases/download"
        f"/v{VARS.BEPINEX_VERSION.value}/BepInEx_unix_{VARS.BEPINEX_VERSION.value}.0.zip "
        "-O .downloads/BepInEx/BepInEx.zip"
    )
    ctx.run("unzip -u .downloads/BepInEx/BepInEx.zip -d .downloads/BepInEx")
    ctx.run("rm .downloads/BepInEx/BepInEx.zip")

    ##################
    # modify BepInEx #
    ##################

    run_bepinex_sh = ".downloads/BepInEx/run_bepinex.sh"
    search_string = 'executable_name=""'
    replacement_string = 'executable_name="Timberborn.app"'
    modified_contents = []

    with open(run_bepinex_sh, "r", encoding="utf-8") as _file:
        file_lines = _file.readlines()
        modified_contents = copy.copy(file_lines)

        target_line = None
        for line_number, line_value in enumerate(file_lines):
            if search_string in line_value:
                target_line = line_number
                modified_contents[line_number] = replacement_string

        if not target_line:
            raise Exception(f"could not find {search_string} within {run_bepinex_sh}")

    with open(run_bepinex_sh, "w", encoding="utf-8") as _file:
        _file.writelines(modified_contents)

    ctx.run(f"chmod a+x {run_bepinex_sh}")

    ######################
    # copy into steamapp #
    ######################

    ctx.run(f"cp -rv .downloads/BepInEx/* {VARS.STEAMAPP.value}")
    ctx.run(
        f"cp assets/config/BepInEx.cfg {VARS.STEAMAPP.value}/BepInEx/config/BepInEx.cfg"
    )


@invoke.task
def setup_timberapi(ctx):
    """
    setup https://github.com/Timberborn-Modding-Central/TimberAPI/releases in the Timberborn folder
    """

    ######################
    # download TimberAPI #
    ######################

    ctx.run("rm -rf .downloads/TimberAPI")
    ctx.run("mkdir -p .downloads/TimberAPI")
    ctx.run(
        "wget "
        "https://github.com/Timberborn-Modding-Central/TimberAPI/archive/refs/tags"
        f"/v{VARS.TIMBERAPI_VERSION.value}.zip "
        "-O .downloads/TimberAPI/TimberAPI.zip"
    )
    ctx.run("unzip -u .downloads/TimberAPI/TimberAPI.zip -d .downloads/TimberAPI")
    ctx.run("rm .downloads/TimberAPI/TimberAPI.zip")
