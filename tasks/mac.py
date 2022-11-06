"""
Mac based build commands
"""

# builtin
import copy


# 3rd party
import invoke


@invoke.task
def setup_bepinex(
    ctx,
    version="5.4.21",
    steamapp=r"~/Library/Application\ Support/Steam/steamapps/common/Timberborn/",
):
    """
    setup https://github.com/BepInEx/BepInEx/releases in the Timberborn folder
    """

    ####################
    # download BepInEx #
    ####################

    ctx.run("rm -rf .downloads/BepInEx")
    ctx.run("mkdir -p .downloads/BepInEx")
    ctx.run(
        "wget -q "
        "https://github.com/BepInEx/BepInEx/releases/download"
        f"/v{version}/BepInEx_unix_{version}.0.zip "
        "-O .downloads/BepInEx/BepInEx.zip"
    )
    ctx.run("unzip .downloads/BepInEx/BepInEx.zip -d .downloads/BepInEx")
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

    ctx.run(f"cp -rv .downloads/BepInEx/* {steamapp}")
