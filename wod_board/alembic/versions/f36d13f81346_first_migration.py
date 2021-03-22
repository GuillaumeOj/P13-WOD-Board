"""First migration

Revision ID: f36d13f81346
Revises: 
Create Date: 2021-03-22 16:26:10.955256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f36d13f81346"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "wod_type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "wod",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("note", sa.String(), nullable=True),
        sa.Column(
            "date", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("wod_type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["wod_type_id"],
            ["wod_type.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "round",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("wod_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["round.id"],
        ),
        sa.ForeignKeyConstraint(
            ["wod_id"],
            ["wod.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("wod_id", "position", name="wod_id_position"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("round")
    op.drop_table("wod")
    op.drop_table("wod_type")
    op.drop_table("user")
    # ### end Alembic commands ###
