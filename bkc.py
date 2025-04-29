import streamlit as st
import hashlib
import datetime
import json
import os

# 📦 Block Class
class Block:
    def __init__(self, index, data, timestamp, previous_hash, hash=None):
        self.index = index
        self.data = data
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = hash or self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'data': self.data,
            'timestamp': str(self.timestamp),
            'previous_hash': self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "data": self.data,
            "timestamp": str(self.timestamp),
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            index=data["index"],
            data=data["data"],
            timestamp=datetime.datetime.fromisoformat(data["timestamp"]),
            previous_hash=data["previous_hash"],
            hash=data["hash"]
        )

# 🔗 Blockchain Class
class ReportCardBlockchain:
    def __init__(self, filename="blockchain.json"):
        self.filename = filename
        self.chain = self.load_chain()

    def create_genesis_block(self):
        return Block(0, {"message": "Genesis Block"}, datetime.datetime.now(), "0")

    def load_chain(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                return [Block.from_dict(block) for block in data]
        else:
            genesis = self.create_genesis_block()
            self.save_chain([genesis])
            return [genesis]

    def save_chain(self, chain=None):
        chain = chain or self.chain
        with open(self.filename, "w") as f:
            json.dump([block.to_dict() for block in chain], f, indent=4)

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
        self.save_chain()

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
            st.code(f"Hash         : {block.hash}")
            st.code(f"Previous Hash: {block.previous_hash}")
            st.markdown("---")

# 🧠 Streamlit App
st.set_page_config(page_title="📚 Report Card Blockchain", layout="wide")
st.title("📚 School Report Card Blockchain with JSON Storage")

# Initialize blockchain and store in session
if "blockchain" not in st.session_state:
    st.session_state.blockchain = ReportCardBlockchain()

blockchain = st.session_state.blockchain

# ➕ Add Report Card Form
with st.form("add_block_form"):
    st.subheader("➕ Add New Student Report Card")
    name = st.text_input("Student Name")
    math = st.selectbox("Math Grade", ["A", "B", "C", "D", "F"])
    science = st.selectbox("Science Grade", ["A", "B", "C", "D", "F"])
    english = st.selectbox("English Grade", ["A", "B", "C", "D", "F"])
    submit = st.form_submit_button("Add to Blockchain")

    if submit:
        if name.strip():
            data = {
                "student_name": name,
                "grades": {
                    "Math": math,
                    "Science": science,
                    "English": english
                }
            }
            blockchain.add_block(data)
            st.success(f"✅ Report card for {name} added.")
        else:
            st.warning("⚠️ Please enter a valid student name.")

# 📜 Display the Blockchain
st.subheader("📜 Blockchain Ledger")
blockchain.display_chain()

# ✅ Validate Blockchain
st.subheader("🔍 Blockchain Integrity Check")
if blockchain.is_chain_valid():
    st.success("✅ Blockchain is valid.")
else:
    st.error("❌ Blockchain has been tampered!")
