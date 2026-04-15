"""Initial schema creation with all core tables.

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-04-13 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create agents table
    op.create_table(
        'agents',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('version', sa.String(50), nullable=False),
        sa.Column('framework', sa.String(100), nullable=False),
        sa.Column('status', sa.Enum('draft', 'active', 'deprecated', 'archived', name='agentstatus'), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('a2a_compliant', sa.Boolean(), nullable=False),
        sa.Column('capabilities', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('config', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('owner_id', sa.String(255), nullable=True),
        sa.Column('namespace', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_agent_name', 'agents', ['name'])
    op.create_index('idx_agent_status', 'agents', ['status'])
    op.create_unique_constraint('uc_agent_ns_name_version', 'agents', ['namespace', 'name', 'version'])

    # Create tools table
    op.create_table(
        'tools',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('category', sa.Enum('http', 'database', 'filesystem', 'messaging', 'custom', name='toolcategory'), nullable=False),
        sa.Column('version', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('input_schema', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('output_schema', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('config', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('auth_type', sa.String(50), nullable=True),
        sa.Column('auth_config', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('health_check_enabled', sa.Boolean(), nullable=False),
        sa.Column('health_check_url', sa.String(500), nullable=True),
        sa.Column('last_health_check', sa.DateTime(), nullable=True),
        sa.Column('is_healthy', sa.Boolean(), nullable=False),
        sa.Column('rate_limit', sa.Integer(), nullable=True),
        sa.Column('namespace', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_tool_name', 'tools', ['name'])
    op.create_index('idx_tool_category', 'tools', ['category'])

    # Create orchestrations table
    op.create_table(
        'orchestrations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('version', sa.String(50), nullable=False),
        sa.Column('status', sa.Enum('draft', 'published', 'deprecated', 'archived', name='orchestrationstatus'), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('dag', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('pattern', sa.String(50), nullable=False),
        sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('config', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('owner_id', sa.String(255), nullable=True),
        sa.Column('namespace', sa.String(100), nullable=False),
        sa.Column('compiled', sa.Boolean(), nullable=False),
        sa.Column('compiled_plan', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_orchestration_name', 'orchestrations', ['name'])
    op.create_index('idx_orchestration_status', 'orchestrations', ['status'])

    # Create executions table
    op.create_table(
        'executions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('orchestration_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.Enum('pending', 'running', 'success', 'failed', 'cancelled', 'timeout', name='executionstatus'), nullable=False),
        sa.Column('phase', sa.Enum('queued', 'initializing', 'executing', 'finalizing', 'completed', name='executionphase'), nullable=False),
        sa.Column('input_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('output_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('state', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('context', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('error', sa.Text(), nullable=True),
        sa.Column('error_details', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('ended_at', sa.DateTime(), nullable=True),
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('triggered_by', sa.String(255), nullable=True),
        sa.Column('parent_execution_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('trace_id', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['orchestration_id'], ['orchestrations.id'], ),
        sa.ForeignKeyConstraint(['parent_execution_id'], ['executions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_execution_status', 'executions', ['status'])
    op.create_index('idx_execution_orchestration', 'executions', ['orchestration_id'])

    # Create execution_logs table
    op.create_table(
        'execution_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('execution_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('level', sa.String(20), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('context', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('node_id', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['execution_id'], ['executions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_execution_log_execution', 'execution_logs', ['execution_id'])

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('changes', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=True),
        sa.Column('request_id', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_audit_entity_type', 'audit_logs', ['entity_type'])
    op.create_index('idx_audit_entity_id', 'audit_logs', ['entity_id'])


def downgrade() -> None:
    op.drop_index('idx_audit_entity_id', table_name='audit_logs')
    op.drop_index('idx_audit_entity_type', table_name='audit_logs')
    op.drop_table('audit_logs')
    op.drop_index('idx_execution_log_execution', table_name='execution_logs')
    op.drop_table('execution_logs')
    op.drop_index('idx_execution_orchestration', table_name='executions')
    op.drop_index('idx_execution_status', table_name='executions')
    op.drop_table('executions')
    op.drop_index('idx_orchestration_status', table_name='orchestrations')
    op.drop_index('idx_orchestration_name', table_name='orchestrations')
    op.drop_table('orchestrations')
    op.drop_index('idx_tool_category', table_name='tools')
    op.drop_index('idx_tool_name', table_name='tools')
    op.drop_table('tools')
    op.drop_unique_constraint('uc_agent_ns_name_version', table_name='agents')
    op.drop_index('idx_agent_status', table_name='agents')
    op.drop_index('idx_agent_name', table_name='agents')
    op.drop_table('agents')
