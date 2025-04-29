import streamlit as st
import hashlib
import datetime
import json

# Define a Block
class Block:
    def __init__(self, index, data, timestamp, previous_hash):
        self.index = index
        self.data = data
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'data': self.data,
            'timestamp': str(self.timestamp),
            'previous_hash': self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

# Define the Blockchain
class ReportCardBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, {"message": "Genesis Block"}, datetime.datetime.now(), "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            data=data,
            timestamp=datetime.datetime.now(),
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def display_chain(self):
        for block in self.chain:
            st.write(f"### 🧱 Block {block.index}")
            st.write(f"**Timestamp:** {block.timestamp}")
            st.write(f"**Student Data:** {block.data}")
            st.write(f"**Hash:** `{block.hash}`")
            st.write(f"**Previous Hash:** `{block.previous_hash}`")
            st.markdown("---")


# Streamlit Interface
st.set_page_config(page_title="📚 School Report Card Blockchain", layout="wide")
st.title("📚 School Report Card Blockchain")

# Initialize Blockchain (store in session state to persist across reruns)
if "report_chain" not in st.session_state:
    st.session_state.report_chain = ReportCardBlockchain()

with st.form("add_report_card"):
    st.subheader("➕ Add New Report Card")
    student_name = st.text_input("Student Name")
    math_grade = st.selectbox("Math Grade", ["A", "B", "C", "D", "F"])
    science_grade = st.selectbox("Science Grade", ["A", "B", "C", "D", "F"])
    english_grade = st.selectbox("English Grade", ["A", "B", "C", "D", "F"])
    submitted = st.form_submit_button("Add to Blockchain")

    if submitted and student_name:
        st.session_state.report_chain.add_block({
            "student_name": student_name,
            "grades": {
                "Math": math_grade,
                "Science": science_grade,
                "English": english_grade
            }
        })
        st.success(f"✅ Report card for {student_name} added to blockchain!")

# Display Blockchain
st.subheader("📜 Blockchain Ledger")
st.session_state.report_chain.display_chain()

# Validate Chain
st.subheader("🔍 Blockchain Validity Check")
is_valid = st.session_state.report_chain.is_chain_valid()
st.success("✅ Blockchain is valid.") if is_valid else st.error("❌ Blockchain has been tampered!")
