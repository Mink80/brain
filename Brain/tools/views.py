from flask import Blueprint, render_template
from Brain.models import HistoryItem

tools_blueprint = Blueprint('tools',__name__,
                            template_folder='templates')

@tools_blueprint.route('/history')
def history():
    history_items = HistoryItem.query.order_by(HistoryItem.id.desc()).limit(25)
    return render_template('/tools/history.html', history_items=history_items)
