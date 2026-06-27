import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
from collections import Counter
import mysql.connector


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="WildGuard AI",
    page_icon="🌿",
    layout="wide"
)


# =========================
# DB CONNECTION
# =========================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Athul5555@",
        database="wildguard_ai"
    )


# =========================
# LOAD MODEL
# =========================
model = YOLO("best_an.pt")


# =========================
# RARE SPECIES
# =========================
rare_animals = {"tiger", "elephant", "leopard"}


# =========================
# UI
# =========================
st.title("🌿 WildGuard AI")
st.subheader("Wildlife Detection System")

video_file = st.file_uploader(
    "🎥 Upload Wildlife Video",
    type=["mp4", "avi", "mov"]
)


if video_file:

    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    cap = cv2.VideoCapture(tfile.name)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    duration = round(total_frames / fps, 2) if fps > 0 else 0

    st.markdown("## 📹 Video Information")

    c1, c2, c3 = st.columns(3)

    c1.metric("Duration", f"{duration} sec")
    c2.metric("Frames", total_frames)
    c3.metric("FPS", round(fps, 2))

    if st.button("🚀 Analyze Video"):

        progress = st.progress(0)

        species_counter = Counter()

        # Store best frame statistics
        max_animals = 0
        best_species_counter = Counter()

        # # Unique tracking IDs
        # seen_ids = set()

        # Store first detected frame
        detected_snapshot = None

        frame_count = 0

        with st.spinner("Analyzing Wildlife Activity..."):

            while cap.isOpened():

                ret, frame = cap.read()

                if not ret:
                    break

                frame_count += 1

                # Process every 30th frame
                if frame_count % 5 == 0:

                    current_species = Counter()

                    results = model(
                        frame,
                        imgsz=960,
                        conf=0.5,
                        iou=0.5,
                        verbose=False,
                    )

                    for r in results:

                        if r.boxes is None:
                            continue

                        # Save first detected frame with annotations
                        if detected_snapshot is None and len(r.boxes) > 0:
                            detected_snapshot = r.plot()

                        for box in r.boxes:

                            conf = float(box.conf)

                            if conf < 0.5:
                                continue

                            cls_id = int(box.cls)
                            class_name = model.names[cls_id]

                            # track_id = box.id

                            # if track_id is None:
                            #     continue

                            # track_id = int(track_id)

                            # # Count unique animals only
                            # if track_id not in seen_ids:

                            #     seen_ids.add(track_id)

                            current_species[class_name] += 1
                        current_total = sum(current_species.values())

                # Keep the frame with maximum animals
                        if current_total > max_animals:

                            max_animals = current_total
                            best_species_counter = current_species.copy()
                        progress.progress(
                        min(frame_count / total_frames, 1.0)
                        )

        cap.release()

        species_counter = best_species_counter
        animal_count = max_animals

        st.success("✅ Analysis Completed Successfully")

        # =========================
        # DETECTION SNAPSHOT
        # =========================
        if detected_snapshot is not None:

            st.markdown("## 📸 Detection Snapshot")

            snapshot_rgb = cv2.cvtColor(
                detected_snapshot,
                cv2.COLOR_BGR2RGB
            )

            st.image(
                snapshot_rgb,
                caption="Detected Wildlife",
                use_container_width=True
            )

        # =========================
        # SUMMARY CALCULATIONS
        # =========================
        species_counter = best_species_counter
        animal_count = max_animals

        rare_found = any(
            species_counter.get(a, 0) > 0
            for a in rare_animals
        )

        # =========================
        # WILDLIFE ACTIVITY SCORE
        # =========================
        activity_score = 0

        # Animal count contribution
        activity_score += animal_count * 10

        # Rare species contribution
        if rare_found:
            activity_score += 20

        activity_score = min(activity_score, 100)

        # =========================
        # ACTIVITY LEVEL
        # =========================
        if activity_score <= 30:
            activity_level = "🟢 Low Activity"

        elif activity_score <= 70:
            activity_level = "🟡 Medium Activity"

        else:
            activity_level = "🔴 High Activity"

        # =========================
        # RESULTS
        # =========================
        st.markdown("## 📊 Analysis Results")

        c1, c2 = st.columns(2)

        c1.metric(
            "Animals Detected",
            animal_count
        )

        c2.metric(
            "Wildlife Activity Score",
            f"{activity_score}%"
        )

        st.info(f"Activity Level: {activity_level}")

        # =========================
        # SPECIES SUMMARY
        # =========================
        st.markdown("## 🐾 Species Summary")

        if species_counter:

            for species, count in sorted(
                species_counter.items(),
                key=lambda x: x[1],
                reverse=True
            ):

                st.info(
                    f"{species.title()} → {count}"
                )

        else:

            st.warning("No wildlife detected.")

        # =========================
        # ALERTS
        # =========================
        st.markdown("## 🚨 Wildlife Alerts")

        if rare_found:
            st.success(
                "Rare Wildlife Species Detected"
            )

        if animal_count > 20:
            st.warning(
                "High Wildlife Activity Detected"
            )

        if animal_count == 0:
            st.error(
                "No Animals Detected"
            )

        # =========================
        # SAVE TO MYSQL
        # =========================
        try:

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO detection_results1
                (
                    animal_count,
                    risk_score,
                    rare_found
                )
                VALUES (%s, %s, %s)
            """, (
                animal_count,
                activity_score,
                rare_found
            ))

            detection_id = cursor.lastrowid

            for species, count in species_counter.items():

                cursor.execute("""
                    INSERT INTO species_results
                    (
                        detection_id,
                        species_name,
                        count
                    )
                    VALUES (%s, %s, %s)
                """, (
                    detection_id,
                    species,
                    count
                ))

            conn.commit()

            cursor.close()
            conn.close()

            st.success(
                "📦 Results Saved to MySQL Successfully"
            )

        except Exception as e:

            st.error(
                f"MySQL Error: {e}"
            )