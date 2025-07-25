"""Ajout marchand_id à Commande et commande à Marchand

Revision ID: 34ad121a00d9
Revises: 
Create Date: 2025-07-09 08:10:21.160885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '34ad121a00d9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('marchands')
    op.drop_table('cles_api')
    op.drop_table('utilisateurs')
    op.drop_index(op.f('ix_commandes_reference'), table_name='commandes')
    op.drop_table('commandes')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('commandes',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('reference', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('articles', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('statut', postgresql.ENUM('EN_ATTENTE', 'VALIDEE', 'ANNULEE', 'EN_COURS', 'LIVREE', name='statutcommande'), autoincrement=False, nullable=True),
    sa.Column('total', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('commandes_pkey'))
    )
    op.create_index(op.f('ix_commandes_reference'), 'commandes', ['reference'], unique=True)
    op.create_table('utilisateurs',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('nom', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('mot_de_passe', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('role', postgresql.ENUM('admin', 'utilisateur', 'marchand', 'livreur', name='role'), autoincrement=False, nullable=False),
    sa.Column('date_creation', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('date_mise_a_jour', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='utilisateurs_pkey'),
    sa.UniqueConstraint('email', name='utilisateurs_email_key', postgresql_include=[], postgresql_nulls_not_distinct=False),
    postgresql_ignore_search_path=False
    )
    op.create_table('cles_api',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('cle', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('nom', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('utilisateur_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('est_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('date_creation', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['utilisateur_id'], ['utilisateurs.id'], name=op.f('cles_api_utilisateur_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('cles_api_pkey')),
    sa.UniqueConstraint('cle', name=op.f('cles_api_cle_key'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    op.create_table('marchands',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('nom', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('adresse', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('contact', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('utilisateur_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['utilisateur_id'], ['utilisateurs.id'], name=op.f('marchands_utilisateur_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('marchands_pkey')),
    sa.UniqueConstraint('utilisateur_id', name=op.f('marchands_utilisateur_id_key'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )
    # ### end Alembic commands ###
