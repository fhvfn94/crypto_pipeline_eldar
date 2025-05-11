from airflow.models import XCom
from airflow.models.baseoperator import BaseOperator
from airflow.utils.session import provide_session
from airflow.utils.trigger_rule import TriggerRule
from airflow.exceptions import AirflowSkipException


class ClearXComsOperator(BaseOperator):
    """
    Simple operator to clear XCom records for specific DagRun.
    """
    def __init__(self, **kwargs):
        trigger_rule = kwargs.pop('trigger_rule', TriggerRule.NONE_FAILED)
        super().__init__(
            do_xcom_push=False,
            trigger_rule=trigger_rule,
            **kwargs)

    @provide_session
    def execute(self, context, session=None):
        deleted = 0
        try:
            deleted = session.query(XCom).filter_by(
                dag_id=self.dag_id,
                run_id=context['run_id']
            ).delete()
            session.commit()
        except:
            session.rollback()

        self.log.info(f"{deleted if deleted else 'NO'} XCOM "
                      f"ENTR{'Y' if deleted == 1 else 'IES'} "
                      f"{'HAS' if deleted == 1 else 'HAVE'} "
                      "BEEN DELETED.")

        if not deleted:
            raise AirflowSkipException