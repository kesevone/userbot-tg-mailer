from typing import Any

from jinja2 import Environment


class Jinja:
    """
    A class for rendering Jinja templates.

    Args:
        text (str): The Jinja template text.
        trim_blocks (bool, optional): Whether to trim the blocks. Defaults to True.
        lstrip_blocks (bool, optional): Whether to lstrip the blocks. Defaults to True.
        enable_async (bool, optional): Whether to enable async rendering. Defaults to True.
        args (Any, optional): The arguments to pass to the template.
        kwargs (Any, optional): The keyword arguments to pass to the template.
    """

    def __init__(
        self,
        text: str,
        trim_blocks: bool = True,
        lstrip_blocks: bool = True,
        **kwargs: Any,
    ) -> None:

        self.kwargs = kwargs
        self.text = text
        self.jinja_env = Environment(
            trim_blocks=trim_blocks, lstrip_blocks=lstrip_blocks, enable_async=True
        )
        self.lstrip_blocks = trim_blocks

    async def render(self) -> str:
        """
        Render the Jinja template.

        Returns:
            str: The rendered template text.
        """

        jinja_text = self.jinja_env.from_string(self.text)
        return await jinja_text.render_async(self.kwargs)
