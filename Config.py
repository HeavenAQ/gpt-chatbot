import os
from dataclasses import asdict, dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class LineConfig:
    access_token: str = os.getenv("LINE_ACCESS_TOKEN") or ""
    channel_secret: str = os.getenv("LINE_CHANNEL_SECRET") or ""

    def __post_init__(self):
        if not self.access_token:
            raise ValueError("LINE_ACCESS_TOKEN environment variable is not set")
        elif not self.channel_secret:
            raise ValueError("LINE_CHANNEL_SECRET environment variable is not set")


@dataclass(frozen=True)
class OpenAiConfig:
    api_key: str = os.getenv("OPENAI_API_KEY") or ""
    assistant_id: str = os.getenv("OPENAI_ASSISTANT_ID") or ""

    def __post_init__(self):
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        elif not self.assistant_id:
            raise ValueError("OPENAI_ASSISTANT_ID environment variable is not set")


@dataclass(frozen=True)
class FirestoreConfig:
    type: str = os.getenv("FIRESTORE_TYPE") or "service_account"
    project_id: str = os.getenv("FIRESTORE_PROJECT_ID") or "badminton-rule-db"
    private_key_id: str = os.getenv("FIRESTORE_PRIVATE_KEY_ID") or ""
    private_key: str = os.getenv("FIRESTORE_PRIVATE_KEY") or ""
    client_email: str = os.getenv("FIRESTORE_CLIENT_EMAIL") or ""
    firesotre_client_id: str = os.getenv("FIRESOTRE_CLIENT_ID") or ""
    auth_url: str = os.getenv("FIRESTORE_AUTH_URL") or ""
    token_uri: str = os.getenv("FIRESTORE_TOKEN_URI") or ""
    auth_provider_x509_cert_url: str = (
        os.getenv("FIRESTORE_AUTH_PROVIDER_X509_CERT_URL") or ""
    )
    client_x509_cert_url: str = os.getenv("FIRESTORE_CLIENT_X509_CERT_URL") or ""
    universe_domain: str = os.getenv("FIRESTORE_UNIVERSE_DOMAIN") or ""

    def __post_init__(self):
        if not self.private_key_id:
            raise ValueError("FIRESTORE_PRIVATE_KEY_ID environment variable is not set")
        elif not self.private_key:
            raise ValueError("FIRESTORE_PRIVATE_KEY environment variable is not set")
        elif not self.client_email:
            raise ValueError("FIRESTORE_CLIENT_EMAIL environment variable is not set")
        elif not self.firesotre_client_id:
            raise ValueError("FIRESOTRE_CLIENT_ID environment variable is not set")
        elif not self.auth_url:
            raise ValueError("FIRESTORE_AUTH_URL environment variable is not set")
        elif not self.token_uri:
            raise ValueError("FIRESTORE_TOKEN_URI environment variable is not set")
        elif not self.auth_provider_x509_cert_url:
            raise ValueError(
                "FIRESTORE_AUTH_PROVIDER_X509_CERT_URL environment variable is not set"
            )
        elif not self.client_x509_cert_url:
            raise ValueError(
                "FIRESTORE_CLIENT_X509_CERT_URL environment variable is not set"
            )
        elif not self.universe_domain:
            raise ValueError(
                "FIRESTORE_UNIVERSE_DOMAIN environment variable is not set"
            )

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True, kw_only=True)
class GPTChatBotConfig:
    line: LineConfig
    openai: OpenAiConfig
    firestore: FirestoreConfig
