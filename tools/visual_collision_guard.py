"""tools/visual_collision_guard.py

Visual Collision and Safe-Zone Guard for Phase 21 Editorial Motion Graphics.
Enforces strict compositional hierarchy, prevents unreadable typography overlaps,
and ensures safe margins across vertical 1080x1920 video.
"""

from typing import Dict, List, Tuple, Any, Optional
import math


# Safe Margins for 1080x1920 portrait video
SAFE_LEFT = 80.0
SAFE_RIGHT = 1000.0
SAFE_TOP = 100.0
SAFE_BOTTOM = 1740.0

# Priority Hierarchy Levels
P0_CTA = 0              # Brand resolution lockup / primary CTA
P1_PRIMARY_SUBJECT = 1  # Central halftone trader figure / hero focal subject
P2_STATISTIC = 2        # Core proof cards (68.4%, 14.6h timeline, 1.48M counter)
P3_CAPTION = 3          # Dynamic editorial captions
P4_ANNOTATION = 4       # FIG. labels, secondary annotations, notification alert pills
P5_DECORATIVE = 5       # Background ticker, tumbling newspapers, micro-charts


class BoundingBox2D:
    """Axis-Aligned Bounding Box in 1080x1920 screen pixel coordinates."""

    def __init__(self, xmin: float, ymin: float, xmax: float, ymax: float, object_id: str, priority: int):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.object_id = object_id
        self.priority = priority

    @property
    def width(self) -> float:
        return max(0.0, self.xmax - self.xmin)

    @property
    def height(self) -> float:
        return max(0.0, self.ymax - self.ymin)

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def center_x(self) -> float:
        return (self.xmin + self.xmax) / 2.0

    @property
    def center_y(self) -> float:
        return (self.ymin + self.ymax) / 2.0

    def intersects(self, other: "BoundingBox2D") -> Tuple[bool, float]:
        """Check if two boxes intersect.
        Returns (is_intersecting, overlap_ratio_relative_to_smaller_box).
        """
        ixmin = max(self.xmin, other.xmin)
        iymin = max(self.ymin, other.ymin)
        ixmax = min(self.xmax, other.xmax)
        iymax = min(self.ymax, other.ymax)

        if ixmax <= ixmin or iymax <= iymin:
            return False, 0.0

        int_area = (ixmax - ixmin) * (iymax - iymin)
        min_area = min(self.area, other.area)
        if min_area <= 0:
            return False, 0.0

        ratio = int_area / min_area
        return ratio > 0.08, ratio

    def check_safe_margins(self) -> Dict[str, Any]:
        """Check if bounding box violates safe boundary limits."""
        violations = []
        if self.xmin < SAFE_LEFT:
            violations.append(f"Left edge {self.xmin:.1f}px < min {SAFE_LEFT}px")
        if self.xmax > SAFE_RIGHT:
            violations.append(f"Right edge {self.xmax:.1f}px > max {SAFE_RIGHT}px")
        if self.ymin < SAFE_TOP:
            violations.append(f"Top edge {self.ymin:.1f}px < min {SAFE_TOP}px")
        if self.ymax > SAFE_BOTTOM:
            violations.append(f"Bottom edge {self.ymax:.1f}px > max {SAFE_BOTTOM}px")
        return {
            "compliant": len(violations) == 0,
            "violations": violations
        }


class VisualCollisionGuard:
    """Audits spatial compositions across time, detects forbidden overlaps,
    and reports layout clearance metrics.
    """

    def __init__(self, width: int = 1080, height: int = 1920):
        self.width = width
        self.height = height

    def get_object_priority(self, obj: Any) -> int:
        """Assign priority class based on object identifier and type."""
        oid = getattr(obj, "id", "")
        otype = getattr(obj, "type", "")

        if "cta" in oid or "brand" in oid:
            return P0_CTA
        if "trader_s1" in oid or "trader_main" in oid or "trader_s7" in oid:
            return P1_PRIMARY_SUBJECT
        if "counter" in oid or "acc_card" in oid or "timeline" in oid or "radar" in oid:
            return P2_STATISTIC
        if "cap_" in oid or "signal_card" in oid or "banner" in oid:
            return P3_CAPTION
        if "fig" in oid or "alert" in oid or "badge" in oid:
            return P4_ANNOTATION
        return P5_DECORATIVE

    def compute_bounding_box(self, obj: Any, camera: Any, t: float) -> Optional[BoundingBox2D]:
        """Calculate screen-space 2D bounding box for an active object at time t."""
        if not obj.is_active(t):
            return None

        # Ensure object transform is updated
        obj.update_at_time(t)
        sx, sy, scale = camera.project(obj.x, obj.y, obj.z)
        final_scale = scale * getattr(obj, "scale_x", 1.0)
        if final_scale <= 0.01:
            return None

        # Determine approximate dimensions
        w = getattr(obj, "w", 400.0)
        h = getattr(obj, "h", 120.0)

        # Special casing for typography & cutouts
        oid = obj.id
        if "trader" in oid:
            w, h = getattr(obj, "w", 400.0), getattr(obj, "h", 620.0)
        elif "cap_" in oid:
            text_len = len(getattr(obj, "text", ""))
            fs = getattr(obj, "font_size", 40)
            w = max(180.0, text_len * fs * 0.58 + 40.0)
            h = fs * 1.5 + 24.0
        elif "fig" in oid:
            text_len = len(getattr(obj, "text", ""))
            w = text_len * 12.0 + 30.0
            h = 36.0
        elif "badge" in oid:
            w, h = 260.0, 70.0
        elif "banner" in oid:
            w, h = 680.0, 110.0
        elif "ticker" in oid:
            w, h = float(self.width), 48.0

        tw = w * final_scale
        th = h * final_scale

        xmin = sx - tw / 2.0
        ymin = sy - th / 2.0
        xmax = sx + tw / 2.0
        ymax = sy + th / 2.0

        prio = self.get_object_priority(obj)
        return BoundingBox2D(xmin, ymin, xmax, ymax, obj.id, prio)

    def audit_frame(self, active_objects: List[Any], camera: Any, t: float) -> Dict[str, Any]:
        """Audit all active objects at time t for collisions and safe margin compliance."""
        boxes: List[BoundingBox2D] = []
        for obj in active_objects:
            b = self.compute_bounding_box(obj, camera, t)
            if b is not None:
                boxes.append(b)

        forbidden_collisions = []
        acceptable_overlaps = []
        margin_violations = []

        # Margin check on P0-P4 objects
        for b in boxes:
            if b.priority <= P4_ANNOTATION:
                m_res = b.check_safe_margins()
                if not m_res["compliant"]:
                    margin_violations.append({
                        "object_id": b.object_id,
                        "priority": b.priority,
                        "violations": m_res["violations"]
                    })

        # Pairwise collision checks
        n = len(boxes)
        for i in range(n):
            for j in range(i + 1, n):
                b1 = boxes[i]
                b2 = boxes[j]

                intersects, ratio = b1.intersects(b2)
                if not intersects:
                    continue

                # Collision severity classification
                p_high = min(b1.priority, b2.priority)
                p_low = max(b1.priority, b2.priority)

                collision_info = {
                    "obj1": b1.object_id,
                    "obj2": b2.object_id,
                    "overlap_ratio": round(ratio, 3),
                    "priority_pair": f"P{b1.priority} vs P{b2.priority}",
                    "t": round(t, 2)
                }

                # Forbidden conditions:
                # 1. Caption (P3) overlapping Primary Subject (P1)
                # 2. Caption (P3) overlapping Statistic (P2)
                # 3. Two Captions (P3) overlapping each other
                # 4. CTA (P0) overlapping anything above P5
                # 5. Annotation (P4) overlapping Caption (P3)
                is_forbidden = False
                reason = ""

                if p_high == P0_CTA and p_low <= P4_ANNOTATION:
                    is_forbidden = True
                    reason = "CTA obstructed by foreground element"
                elif p_high == P1_PRIMARY_SUBJECT and p_low == P3_CAPTION and ratio > 0.12:
                    is_forbidden = True
                    reason = "Caption directly overlaps primary subject silhouette"
                elif p_high == P2_STATISTIC and p_low == P3_CAPTION and ratio > 0.10:
                    is_forbidden = True
                    reason = "Caption directly overlaps core data statistic"
                elif b1.priority == P3_CAPTION and b2.priority == P3_CAPTION and ratio > 0.10:
                    is_forbidden = True
                    reason = "Two captions occupy identical layout zone"
                elif p_high == P3_CAPTION and p_low == P4_ANNOTATION and ratio > 0.20:
                    is_forbidden = True
                    reason = "Editorial annotation collides with primary caption"

                if is_forbidden:
                    collision_info["reason"] = reason
                    forbidden_collisions.append(collision_info)
                else:
                    acceptable_overlaps.append(collision_info)

        return {
            "time_sec": round(t, 2),
            "active_objects_count": len(boxes),
            "forbidden_collisions": forbidden_collisions,
            "acceptable_overlaps_count": len(acceptable_overlaps),
            "margin_violations": margin_violations,
            "compliant": len(forbidden_collisions) == 0 and len(margin_violations) == 0
        }

    def audit_composition(self, comp: Any, sample_step_sec: float = 0.5) -> Dict[str, Any]:
        """Perform full timeline audit across entire composition."""
        total_samples = int(comp.duration / sample_step_sec) + 1
        timeline_results = []
        all_forbidden = []
        all_margin_issues = []

        for i in range(total_samples):
            t = min(comp.duration, i * sample_step_sec)
            active = [obj for obj in comp.objects if obj.is_active(t)]
            res = self.audit_frame(active, comp.camera, t)
            if not res["compliant"]:
                all_forbidden.extend(res["forbidden_collisions"])
                all_margin_issues.extend(res["margin_violations"])
            timeline_results.append(res)

        # De-duplicate issues
        unique_forbidden = []
        seen_pairs = set()
        for c in all_forbidden:
            key = tuple(sorted([c["obj1"], c["obj2"]]))
            if key not in seen_pairs:
                seen_pairs.add(key)
                unique_forbidden.append(c)

        is_clean = len(unique_forbidden) == 0 and len(all_margin_issues) == 0
        return {
            "status": "PASS" if is_clean else "COLLISIONS_DETECTED",
            "total_samples_audited": total_samples,
            "sampling_interval_sec": sample_step_sec,
            "forbidden_collisions_count": len(unique_forbidden),
            "forbidden_collisions": unique_forbidden,
            "margin_violations_count": len(all_margin_issues),
            "margin_violations": all_margin_issues[:10]
        }
