# Nine Men's Morris Game 🎮  
AI powered classic board game with GUI and testing
# Nine Men's Morris Game 🎮  
A strategic two-player board game implemented in Python with an intelligent AI opponent. Developed over three sprints, the game combines traditional gameplay with modern algorithms to deliver an engaging experience through a Tkinter-based GUI.

---

## 🧠 The Strategy Behind the AI

The heart of the computer-controlled opponent is the **Minimax algorithm with Alpha-Beta Pruning**, designed to simulate intelligent thinking, predict player moves, and make optimal decisions at every stage of the game.

### 🌟 Key Features:
- Strategic AI powered by Minimax with alpha-beta pruning
- Adaptive decision-making across all game phases
- Visual, user-friendly interface built with Tkinter
- Game logic handled through well-structured Python classes
- Unit-tested for quality and fairness

---

## 🎮 Game Phases & AI Behavior

1. **Placing Phase (Phase 1)**  
   - AI tries to form “mills” or block opponent’s mills during piece placement.
2. **Moving Phase (Phase 2)**  
   - AI evaluates adjacent moves, mill opportunities, and defensive tactics.
3. **Flying Phase (Phase 3)**  
   - When reduced to 3 pieces, AI flies to any open spot to maximize strategic advantage.

---

## 📊 AI Decision-Making Process

The AI uses a heuristic evaluation function that scores board states by analyzing:
- Piece count difference
- Number of mills formed
- Potential mill setups and threats
- Mobility and control of key positions

---

## 💻 Technologies Used

| Component        | Technology       |
|------------------|------------------|
| Programming      | Python           |
| GUI              | Tkinter          |
| AI               | Minimax + Alpha-Beta Pruning |
| Testing          | unittest module  |
| Development Tool | Git & GitHub     |

---

## 🧪 Testing for Reliability

Tests are written in `test_game.py` to verify:
- Correct piece placements
- Mill formation and removal
- Victory conditions
- Adherence to turn logic and rules

---

## 📂 Project Structure

nine-mens-morris-game/
├── sprint_1/
│ ├── main.py
│ ├── game_logic.py
│ ├── gui.py
│ ├── utils.py
│ └── test_game.py
├── docs/
│ ├── Sprint3_Individual_Report_Sumayya.docx
│ └── Sprint3_Team_Report.docx
├── README.md

yaml
Copy
Edit

---

## 🚀 Future Enhancements

- Dynamic depth adjustment for smarter move evaluation
- Opening move library to save computing time
- Game history learning for improved adaptability

---

## 👤 Author

**Sumayya Fathima Shaik**  
Master’s in Computer Science @ University of Missouri–Kansas City  
Ex-Associate Software Engineer @ Accenture  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/sumayya-fathima-shaik-945709210)

---

## 📜 License

This project is licensed under the **MIT License**. Feel free to use and modify.

---

## 🙌 Acknowledgment

This project is part of an academic sprint series focused on combining software engineering principles with algorithmic problem-solving. Special thanks to my team members and mentors for feedback and collaboration.