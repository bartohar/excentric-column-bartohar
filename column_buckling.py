def find_critical_load(L, E, A, r, c, e, sigma_allow):
    """
    L: אורך במ"מ
    E: מודול אלסטיות ב-MPa
    A: שטח חתך בממ"ר
    r: רדיוס אינרציה במ"מ
    c: מרחק לסיב קיצוני במ"מ
    e: אקסצנטריות במ"מ
    sigma_allow: מאמץ מותר ב-MPa

    Return: העומס P בניוטון (float)
    """
    # כתimport numpy as np
from scipy.optimize import bisect

def find_critical_load(L, E, A, r, c, e, sigma_allow):
    """
    L: אורך במ"מ
    E: מודול אלסטיות ב-MPa
    A: שטח חתך בממ"ר
    r: רדיוס אינרציה במ"מ
    c: מרחק לסיב קיצוני במ"מ
    e: אקסצנטריות במ"מ
    sigma_allow: מאמץ מותר ב-MPa
    
    Return: העומס P בניוטון (float)
    """
    
    # 1. הגדרת פונקציית המטרה: f(P) = sigma_max(P) - sigma_allow
    def f(P):
        # אם P הוא 0, המאמץ הוא 0 (מונע חלוקה באפס או שורש של אפס במקרים מסוימים)
        if P <= 0:
            return -sigma_allow
        
        # חישוב הארגומנט שבתוך ה-cos
        # הארגומנט: (L / (2 * r)) * sqrt(P / (E * A))
        angle = (L / (2 * r)) * np.sqrt(P / (E * A))
        
        # חישוב הסקנט: sec(x) = 1 / cos(x)
        sec_val = 1 / np.cos(angle)
        
        # נוסחת הסקנט למאמץ מקסימלי
        sigma_max = (P / A) * (1 + (e * c / r**2) * sec_val)
        
        return sigma_max - sigma_allow

    # 2. קביעת גבולות לחיפוש הנומרי (Bracketing)
    # הגבול התחתון הוא עומס אפסי כמעט
    p_min = 1e-5 
    
    # הגבול העליון התיאורטי הוא עומס אוילר: P_euler = (pi^2 * E * I) / L^2
    # מכיוון ש- I = A * r^2:
    p_euler = (np.pi**2 * E * A * r**2) / L**2
    
    # כדי למנוע אסימפטוטה (שבה הקוסינוס מתאפס ב- pi/2), נבחר חסם עליון מעט קטן מעומס אוילר
    p_max = p_euler * 0.999
    
    # 3. הרצת שיטת החצייה למציאת השורש ברמת דיוק גבוהה
    critical_load = bisect(f, p_min, p_max, xtol=1e-5)
    
    return float(critical_load)בו כאן את הקוד
