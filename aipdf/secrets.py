import keyring
import typer
from typing_extensions import Annotated

app = typer.Typer()


def get_secret(service: str) -> str:
    """
    Get a secret from the keyring.

    Note: This is not really secure, but compared to storing the secret in plaintext,
    this is the lesser evil.

    Note: This function will raise an exception if the secret is not set.

    Parameters
    ----------
    service : str
        The name of the service to get the secret for.

    Returns
    -------
    str
        The secret for the service.
    """
    secret = keyring.get_password(service, "api-key")
    if secret is None:
        raise Exception("Secret not set")
    return secret


def set_secret(service: str, secret: str, force: bool) -> None:
    """
    Set a secret in the keyring.

    Note that this function will raise an exception if the secret is already set and
    the set operation is not forced.

    Parameters
    ----------
    service : str
        The name of the service to set the secret for.

    secret : str
        The secret to set.

    force : bool
        Whether to overwrite the secret if it already exists.

    Returns
    -------
    None
    """

    # Check if the secret is already set
    if get_secret(service) is None:
        if not force:
            raise Exception("Secret already set, you can overrite with --force")
        else:
            print("Secret already set, overwriting...")

    # Set the secret
    keyring.set_password(service, "api-key", secret)


@app.command()
def set(
    service: Annotated[str, typer.Option("--service", "-s", help="Service Name")],
    secret: Annotated[str, typer.Option("--key", "-k", help="Service Name")],
    force: Annotated[bool, typer.Option("--force")] = False,
) -> None:
    """
    Set a secret in the keyring.

    Parameters
    ----------
    service : str
        The name of the service to set the secret for.

    secret : str
        The secret to set.

    force : bool
        Whether to overwrite the secret if it already exists.

    Returns
    -------
    None
    """
    set_secret(service, secret, force)


@app.command()
def get(
    service: Annotated[str, typer.Option("--service", "-s", help="Service Name")]
) -> None:
    """
    Get a secret from the keyring.

    Note: This is not really secure, but compared to storing the secret in plaintext,
    this is the lesser evil.

    Parameters
    ----------
    service : str
        The name of the service to get the secret for.

    Returns
    -------
    str
        The secret for the service.
    """
    typer.echo(get_secret(service))


if __name__ == "__main__":
    app()
