from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import io
import calendar

app = Flask(__name__)

questions = [
    "What are the most important outcomes we want from faculty meetings this year?",
    "How can our faculty meetings align with our school or district priorities?",
    "What do we want staff to know, feel, and do as a result of each meeting?",
    "How often should we meet, and how long should each meeting be?",
    "How can we balance whole-faculty time with grade-level, department, or interdisciplinary collaboration?",
    "What recurring themes or initiatives (e.g., instruction, data use, PBIS, PBL) should we thread throughout the year?",
    "How can we use meeting time to deepen professional learning rather than just disseminating information?",
    "How can we increase teacher engagement and participation during meetings?",
    "How might we include teacher-led sessions, roundtables, or peer sharing?",
    "What opportunities will there be for teachers to reflect, provide input, or co-create next steps?",
    "What standing agenda items (e.g., celebrations, student data snapshots, norms review) should be included regularly?",
    "How will we communicate agendas in advance and ensure clarity of expectations?",
    "Who will be responsible for facilitating or supporting each meeting?",
    "How will we follow up on the work done during faculty meetings?",
    "How can we measure the impact of our meetings on teaching and learning?",
    "How will we gather feedback on meetings and adjust accordingly?"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        responses = [request.form.get(f'q{i}', '') for i in range(len(questions))]
        plan = generate_plan(responses)
        return render_template('result.html', plan=plan)
    return render_template('form.html', questions=questions)

@app.route('/download', methods=['POST'])
def download():
    plan_text = request.form['plan']
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in plan_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return send_file(pdf_output, as_attachment=True, download_name="faculty_meeting_plan.pdf", mimetype='application/pdf')

def generate_plan(responses):
    months = list(calendar.month_name)[1:]
    plan = ""
    for i, month in enumerate(months):
        plan += f"{month} Faculty Meeting:\n"
        plan += f"- Focus: {responses[0]} aligned with {responses[1]}\n"
        plan += f"- Objectives: {responses[2]}\n"
        plan += f"- Format: {responses[3]} | Collaboration: {responses[4]}\n"
        plan += f"- Themes: {responses[5]}\n"
        plan += f"- Learning Approach: {responses[6]}\n"
        plan += f"- Engagement: {responses[7]}\n"
        plan += f"- Teacher Involvement: {responses[8]}\n"
        plan += f"- Reflection/Input: {responses[9]}\n"
        plan += f"- Agenda Items: {responses[10]}\n"
        plan += f"- Communication: {responses[11]}\n"
        plan += f"- Facilitator: {responses[12]}\n"
        plan += f"- Follow-up: {responses[13]}\n"
        plan += f"- Impact Measurement: {responses[14]}\n"
        plan += f"- Feedback: {responses[15]}\n\n"
    return plan

if __name__ == '__main__':
    app.run(debug=True)
