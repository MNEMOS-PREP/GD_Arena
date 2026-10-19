"""evaluation job: when a job held up by the model allowance runs again

Revision ID: 0006_evaluation_retry_after
Revises: 0005_modes_and_turns
Create Date: 2026-10-19
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0006_evaluation_retry_after"
down_revision: str | None = "0005_modes_and_turns"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "evaluation_jobs",
        sa.Column("retry_after", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("evaluation_jobs", "retry_after")
