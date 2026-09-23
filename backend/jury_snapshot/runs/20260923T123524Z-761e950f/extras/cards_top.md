GID: #100000008603629100
Роль: coordinator
Вход: 1,817,300 ₸; выход: 4,986,156 ₸.
Отправителей: 19; получателей: 61.
Соответствие роли: 1.0; приоритет: 1.0.
Основание: Связующий узел: посредничество ≥ p99, 9 других кластеров, 13 хабов; вход 1,8 млн ₸, выход 5,0 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "coordinator", "role_score": 1.0, "priority_score": 1.0, "priority_rank": 1, "rule_id": "R_COORD", "rule_text": "betweenness >= 0.0019892319141409562; n_nbr_clusters >= 2; max(up_hubs, down_hubs) >= 2", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 19, "out_deg": 61, "in_kzt": 1817300.0, "out_kzt": 4986156.0, "pass_through": 2.7437165025037142, "depth": 2, "betweenness": 0.00576052874226788, "n_nbr_clusters": 9, "up_hubs": 13, "down_hubs": 12}, "alternatives": [{"role": "distributor", "rule_id": "R_DIST", "strength": 6.1}, {"role": "consolidator", "rule_id": "R_CONS", "strength": 3.8}]}

Связи: {"cluster_id": 6, "cluster": {"cluster_id": 6, "n_nodes": 106, "n_seed": 0, "sum_kzt_internal": 11794744.0, "top_gids": ["100000008603629100", "100000001857829100", "100000000661912100", "100000003880331100", "100000002723538100"], "hypothesis": "Фрагмент без seed на 1-м колене; назначение не определено", "hypothesis_rule": "H_NOSEED", "role_counts": {"consolidator": 0, "distributor": 3, "transit": 3, "terminal": 1, "coordinator": 1, "peripheral": 98}, "component_ids": [0]}, "nearest_hub": "100000004351795100", "path": ["100000008603629100", "100000004351795100"], "n_nbr_clusters": 9}

Время: {"fast_matched_kzt": 1817300.0, "fast_pass_share": 1.0, "median_hold_days": 0, "burst_score": 2.495798319327731, "burst": false, "active_days": 27, "first_date": "2026-07-03", "last_date": "2026-07-31", "fast_transit": true, "max_senders_same_day": 4, "sync_in_days": 5, "max_recipients_same_day": 7, "sync_out_days": 4}

Маршруты: {"n_cycles": 762, "n_time_consistent_cycles": 96, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00028", "length": 2, "cycle_type": "reciprocal", "path": "100000001138283100→100000008603629100→100000001138283100", "min_edge_kzt": 40000.0, "total_kzt": 121805.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00052", "length": 2, "cycle_type": "reciprocal", "path": "100000001857829100→100000008603629100→100000001857829100", "min_edge_kzt": 26000.0, "total_kzt": 434000.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00073", "length": 2, "cycle_type": "reciprocal", "path": "100000002723538100→100000008603629100→100000002723538100", "min_edge_kzt": 70647.0, "total_kzt": 155647.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}], "total": 775, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier", "split"], "examples": {"items": [{"anomaly_id": "A00075", "gid": "100000003880331100", "anomaly_type": "split_pair", "feature": "n_tx_window", "value": 6.0, "reference": 0.007478488219062841, "ratio": null, "counterparty_gid": "100000008603629100", "description": "Похожие суммы в коротком окне; дробление ниже 5 000 ₸ в данных не видно."}, {"anomaly_id": "A00132", "gid": "100000005910114100", "anomaly_type": "split_pair", "feature": "n_tx_window", "value": 6.0, "reference": 0.14443459328032696, "ratio": null, "counterparty_gid": "100000008603629100", "description": "Похожие суммы в коротком окне; дробление ниже 5 000 ₸ в данных не видно."}, {"anomaly_id": "A00146", "gid": "100000007639767100", "anomaly_type": "split_pair", "feature": "n_tx_window", "value": 3.0, "reference": 0.027483467306845453, "ratio": null, "counterparty_gid": "100000008603629100", "description": "Похожие суммы в коротком окне; дробление ниже 5 000 ₸ в данных не видно."}], "total": 8, "truncated": true, "available": true}}

Что проверить дальше: ["Переводы ниже 5 000 ₸ по указанным узлам и парам", "Входящие переводы, включая межбанковские и пополнения наличными"]

---

GID: #100000000331309100
Роль: coordinator
Вход: 984,635 ₸; выход: 23,001,375 ₸.
Отправителей: 5; получателей: 99.
Соответствие роли: 1.0; приоритет: 0.995512.
Основание: Связующий узел: посредничество ≥ p99, 13 других кластеров, 8 хабов; вход 984,6 тыс ₸, выход 23,0 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "coordinator", "role_score": 1.0, "priority_score": 0.995512, "priority_rank": 2, "rule_id": "R_COORD", "rule_text": "betweenness >= 0.0019892319141409562; n_nbr_clusters >= 2; max(up_hubs, down_hubs) >= 2", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 5, "out_deg": 99, "in_kzt": 984635.0, "out_kzt": 23001375.0, "pass_through": 23.360306103276848, "depth": 2, "betweenness": 0.0045572340502675075, "n_nbr_clusters": 13, "up_hubs": 3, "down_hubs": 8}, "alternatives": [{"role": "distributor", "rule_id": "R_DIST", "strength": 9.9}, {"role": "consolidator", "rule_id": "R_CONS", "strength": 1.0}]}

Связи: {"cluster_id": 5, "cluster": {"cluster_id": 5, "n_nodes": 126, "n_seed": 0, "sum_kzt_internal": 24907250.33, "top_gids": ["100000000331309100", "100000000332284100", "100000008560717100", "100000003741418100", "100000006734214100"], "hypothesis": "Фрагмент без seed на 1-м колене; назначение не определено", "hypothesis_rule": "H_NOSEED", "role_counts": {"consolidator": 5, "distributor": 2, "transit": 3, "terminal": 11, "coordinator": 1, "peripheral": 104}, "component_ids": [0]}, "nearest_hub": "100000003115284100", "path": ["100000000331309100", "100000003115284100"], "n_nbr_clusters": 13}

Время: {"fast_matched_kzt": 984635.0, "fast_pass_share": 1.0, "median_hold_days": 0, "burst_score": 3.4626865671641793, "burst": true, "active_days": 29, "first_date": "2026-07-01", "last_date": "2026-07-31", "fast_transit": true, "max_senders_same_day": 3, "sync_in_days": 1, "max_recipients_same_day": 15, "sync_out_days": 8}

Маршруты: {"n_cycles": 32, "n_time_consistent_cycles": 1, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00223", "length": 4, "cycle_type": "cycle", "path": "100000000331309100→100000008686313100→100000000437046100→100000001279272100→100000000331309100", "min_edge_kzt": 29200.0, "total_kzt": 782242.0, "has_seed": false, "time_consistent": false, "kind": "cycle"}, {"cycle_id": "C00224", "length": 4, "cycle_type": "cycle", "path": "100000000331309100→100000008686313100→100000006866783100→100000004403675100→100000000331309100", "min_edge_kzt": 47187.0, "total_kzt": 527764.0, "has_seed": true, "time_consistent": false, "kind": "cycle"}, {"cycle_id": "C00392", "length": 5, "cycle_type": "cycle", "path": "100000000331309100→100000008686313100→100000008603629100→100000001857829100→100000003880331100→100000000331309100", "min_edge_kzt": 55500.0, "total_kzt": 1256542.0, "has_seed": false, "time_consistent": false, "kind": "cycle"}], "total": 39, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier", "split"], "examples": {"items": [{"anomaly_id": "A00004", "gid": "100000000331309100", "anomaly_type": "depth_outlier", "feature": "out_deg", "value": 99.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00005", "gid": "100000000331309100", "anomaly_type": "depth_outlier", "feature": "out_kzt", "value": 23001375.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00006", "gid": "100000000331309100", "anomaly_type": "depth_outlier", "feature": "out_tx", "value": 126.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}], "total": 4, "truncated": true, "available": true}}

Что проверить дальше: ["Переводы ниже 5 000 ₸ по указанным узлам и парам", "Входящие переводы, включая межбанковские и пополнения наличными"]

---

GID: #100000005910114100
Роль: coordinator
Вход: 326,144 ₸; выход: 1,469,993 ₸.
Отправителей: 3; получателей: 19.
Соответствие роли: 1.0; приоритет: 0.967913.
Основание: Связующий узел: посредничество ≥ p99, 6 других кластеров, 12 хабов; вход 326,1 тыс ₸, выход 1,5 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "coordinator", "role_score": 1.0, "priority_score": 0.967913, "priority_rank": 3, "rule_id": "R_COORD", "rule_text": "betweenness >= 0.0019892319141409562; n_nbr_clusters >= 2; max(up_hubs, down_hubs) >= 2", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 3, "out_deg": 19, "in_kzt": 326144.0, "out_kzt": 1469993.0, "pass_through": 4.507190075549451, "depth": 3, "betweenness": 0.005842206056572952, "n_nbr_clusters": 6, "up_hubs": 3, "down_hubs": 12}, "alternatives": [{"role": "distributor", "rule_id": "R_DIST", "strength": 1.9}]}

Связи: {"cluster_id": 0, "cluster": {"cluster_id": 0, "n_nodes": 277, "n_seed": 1, "sum_kzt_internal": 31227334.24, "top_gids": ["100000005910114100", "100000000437046100", "100000008477350100", "100000004400305100", "100000002398779100"], "hypothesis": "Смешанная структура: consolidator=9, distributor=3, transit=11, terminal=8, coordinator=9, peripheral=237; требуется ручной разбор", "hypothesis_rule": "H_MIXED", "role_counts": {"consolidator": 9, "distributor": 3, "transit": 11, "terminal": 8, "coordinator": 9, "peripheral": 237}, "component_ids": [0]}, "nearest_hub": "100000008603629100", "path": ["100000005910114100", "100000008603629100"], "n_nbr_clusters": 6}

Время: {"fast_matched_kzt": 266160.0, "fast_pass_share": 0.816081240188383, "median_hold_days": 0, "burst_score": 2.3728813559322033, "burst": false, "active_days": 20, "first_date": "2026-07-01", "last_date": "2026-07-21", "fast_transit": true, "max_senders_same_day": 1, "sync_in_days": 0, "max_recipients_same_day": 5, "sync_out_days": 1}

Маршруты: {"n_cycles": 255, "n_time_consistent_cycles": 25, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00284", "length": 4, "cycle_type": "cycle", "path": "100000001660397100→100000008477350100→100000005910114100→100000006866783100→100000001660397100", "min_edge_kzt": 12000.0, "total_kzt": 413979.0, "has_seed": true, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00285", "length": 4, "cycle_type": "cycle", "path": "100000001660397100→100000008477350100→100000005910114100→100000008603629100→100000001660397100", "min_edge_kzt": 12000.0, "total_kzt": 414891.0, "has_seed": false, "time_consistent": false, "kind": "cycle"}, {"cycle_id": "C00290", "length": 4, "cycle_type": "cycle", "path": "100000001857829100→100000008121806100→100000008346837100→100000005910114100→100000001857829100", "min_edge_kzt": 5000.0, "total_kzt": 213044.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}], "total": 271, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier", "split"], "examples": {"items": [{"anomaly_id": "A00127", "gid": "100000005910114100", "anomaly_type": "depth_outlier", "feature": "out_deg", "value": 19.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00128", "gid": "100000005910114100", "anomaly_type": "depth_outlier", "feature": "out_tx", "value": 56.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00129", "gid": "100000005910114100", "anomaly_type": "split_pair", "feature": "n_tx_window", "value": 3.0, "reference": 0.05067205371092665, "ratio": null, "counterparty_gid": "100000003684369100", "description": "Похожие суммы в коротком окне; дробление ниже 5 000 ₸ в данных не видно."}], "total": 6, "truncated": true, "available": true}}

Что проверить дальше: ["Переводы ниже 5 000 ₸ по указанным узлам и парам"]

---

GID: #100000008165763100
Роль: consolidator
Вход: 1,165,815 ₸; выход: 1,267,858 ₸.
Отправителей: 15; получателей: 17.
Соответствие роли: 1.0; приоритет: 0.961261.
Основание: Признаки консолидации: 15 отправителей (порог 5); вход 1,2 млн ₸, выход 1,3 млн ₸

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "consolidator", "role_score": 1.0, "priority_score": 0.961261, "priority_rank": 4, "rule_id": "R_CONS", "rule_text": "in_deg >= 5", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 15, "out_deg": 17, "in_kzt": 1165815.0, "out_kzt": 1267858.0, "pass_through": 1.087529324978663, "depth": 1, "betweenness": 0.0003452940332330958, "n_nbr_clusters": 7, "up_hubs": 10, "down_hubs": 2}, "alternatives": [{"role": "distributor", "rule_id": "R_DIST", "strength": 1.7}, {"role": "transit", "rule_id": "R_TRANS", "strength": 1.5623533751066847}]}

Связи: {"cluster_id": 3, "cluster": {"cluster_id": 3, "n_nodes": 146, "n_seed": 3, "sum_kzt_internal": 19519090.0, "top_gids": ["100000008165763100", "100000008304139100", "100000004847758100", "100000005830339100", "100000003249054100"], "hypothesis": "Признаки сбора средств от 3 seed с концентрацией у 100000008165763100", "hypothesis_rule": "H_COLLECT", "role_counts": {"consolidator": 3, "distributor": 5, "transit": 3, "terminal": 13, "coordinator": 1, "peripheral": 121}, "component_ids": [0]}, "nearest_hub": "100000003115284100", "path": ["100000008165763100", "100000003115284100"], "n_nbr_clusters": 7}

Время: {"fast_matched_kzt": 630870.0, "fast_pass_share": 0.541140747031047, "median_hold_days": 0, "burst_score": 2.116279069767442, "burst": false, "active_days": 13, "first_date": "2026-07-08", "last_date": "2026-07-28", "fast_transit": true, "max_senders_same_day": 4, "sync_in_days": 3, "max_recipients_same_day": 3, "sync_out_days": 0}

Маршруты: {"n_cycles": 0, "n_time_consistent_cycles": 0, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [], "total": 0, "truncated": false, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier", "split"], "examples": {"items": [{"anomaly_id": "A00085", "gid": "100000004140487100", "anomaly_type": "split_pair", "feature": "n_tx_window", "value": 3.0, "reference": 0.10101525445522108, "ratio": null, "counterparty_gid": "100000008165763100", "description": "Похожие суммы в коротком окне; дробление ниже 5 000 ₸ в данных не видно."}, {"anomaly_id": "A00148", "gid": "100000008165763100", "anomaly_type": "depth_outlier", "feature": "in_deg", "value": 15.0, "reference": 1.0, "ratio": 15.0, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00149", "gid": "100000008165763100", "anomaly_type": "depth_outlier", "feature": "in_tx", "value": 26.0, "reference": 1.0, "ratio": 26.0, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}], "total": 3, "truncated": false, "available": true}}

Что проверить дальше: ["Переводы ниже 5 000 ₸ по указанным узлам и парам"]

---

GID: #100000008346837100
Роль: coordinator
Вход: 254,359 ₸; выход: 1,258,643 ₸.
Отправителей: 9; получателей: 25.
Соответствие роли: 1.0; приоритет: 0.959466.
Основание: Связующий узел: посредничество ≥ p99, 7 других кластеров, 4 хабов; вход 254,4 тыс ₸, выход 1,3 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "coordinator", "role_score": 1.0, "priority_score": 0.959466, "priority_rank": 5, "rule_id": "R_COORD", "rule_text": "betweenness >= 0.0019892319141409562; n_nbr_clusters >= 2; max(up_hubs, down_hubs) >= 2", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 9, "out_deg": 25, "in_kzt": 254359.0, "out_kzt": 1258643.0, "pass_through": 4.948293553599441, "depth": 2, "betweenness": 0.008981156281324022, "n_nbr_clusters": 7, "up_hubs": 4, "down_hubs": 4}, "alternatives": [{"role": "distributor", "rule_id": "R_DIST", "strength": 2.5}, {"role": "consolidator", "rule_id": "R_CONS", "strength": 1.8}]}

Связи: {"cluster_id": 13, "cluster": {"cluster_id": 13, "n_nodes": 52, "n_seed": 5, "sum_kzt_internal": 4171441.0, "top_gids": ["100000008346837100", "100000005074393100", "100000000489417100", "100000008733194100", "100000008003034100"], "hypothesis": "Признаки сбора средств от 5 seed с концентрацией у 100000008346837100", "hypothesis_rule": "H_COLLECT", "role_counts": {"consolidator": 0, "distributor": 0, "transit": 2, "terminal": 0, "coordinator": 2, "peripheral": 48}, "component_ids": [0]}, "nearest_hub": "100000005910114100", "path": ["100000008346837100", "100000005910114100"], "n_nbr_clusters": 7}

Время: {"fast_matched_kzt": 210550.0, "fast_pass_share": 0.8277670536525148, "median_hold_days": 0, "burst_score": 2.368421052631579, "burst": false, "active_days": 15, "first_date": "2026-07-02", "last_date": "2026-07-22", "fast_transit": true, "max_senders_same_day": 4, "sync_in_days": 1, "max_recipients_same_day": 4, "sync_out_days": 0}

Маршруты: {"n_cycles": 111, "n_time_consistent_cycles": 20, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00143", "length": 2, "cycle_type": "reciprocal", "path": "100000005048668100→100000008346837100→100000005048668100", "min_edge_kzt": 6500.0, "total_kzt": 13500.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00162", "length": 2, "cycle_type": "reciprocal", "path": "100000007593823100→100000008346837100→100000007593823100", "min_edge_kzt": 5000.0, "total_kzt": 10800.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00234", "length": 4, "cycle_type": "cycle", "path": "100000000437046100→100000004070318100→100000008346837100→100000004351795100→100000000437046100", "min_edge_kzt": 29511.0, "total_kzt": 721570.0, "has_seed": false, "time_consistent": false, "kind": "cycle"}], "total": 112, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier"], "examples": {"items": [{"anomaly_id": "A00156", "gid": "100000008346837100", "anomaly_type": "depth_outlier", "feature": "in_deg", "value": 9.0, "reference": 1.0, "ratio": 9.0, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}], "total": 1, "truncated": false, "available": true}}

Что проверить дальше: ["Проверить полноту контрагентов и операций за пределами среза."]

---

GID: #100000000437046100
Роль: coordinator
Вход: 1,107,200 ₸; выход: 7,606,224 ₸.
Отправителей: 9; получателей: 42.
Соответствие роли: 0.8508; приоритет: 0.956589.
Основание: Связующий узел: посредничество ≥ p99, 8 других кластеров, 11 хабов; вход 1,1 млн ₸, выход 7,6 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "coordinator", "role_score": 0.8508, "priority_score": 0.956589, "priority_rank": 6, "rule_id": "R_COORD", "rule_text": "betweenness >= 0.0019892319141409562; n_nbr_clusters >= 2; max(up_hubs, down_hubs) >= 2", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 9, "out_deg": 42, "in_kzt": 1107200.0, "out_kzt": 7606224.0, "pass_through": 6.86978323699422, "depth": 2, "betweenness": 0.002197148494797041, "n_nbr_clusters": 8, "up_hubs": 6, "down_hubs": 11}, "alternatives": [{"role": "distributor", "rule_id": "R_DIST", "strength": 4.2}, {"role": "consolidator", "rule_id": "R_CONS", "strength": 1.8}]}

Связи: {"cluster_id": 0, "cluster": {"cluster_id": 0, "n_nodes": 277, "n_seed": 1, "sum_kzt_internal": 31227334.24, "top_gids": ["100000005910114100", "100000000437046100", "100000008477350100", "100000004400305100", "100000002398779100"], "hypothesis": "Смешанная структура: consolidator=9, distributor=3, transit=11, terminal=8, coordinator=9, peripheral=237; требуется ручной разбор", "hypothesis_rule": "H_MIXED", "role_counts": {"consolidator": 9, "distributor": 3, "transit": 11, "terminal": 8, "coordinator": 9, "peripheral": 237}, "component_ids": [0]}, "nearest_hub": "100000008603629100", "path": ["100000000437046100", "100000008603629100"], "n_nbr_clusters": 8}

Время: {"fast_matched_kzt": 992368.0, "fast_pass_share": 0.89628612716763, "median_hold_days": 0, "burst_score": 2.7096774193548385, "burst": false, "active_days": 21, "first_date": "2026-07-10", "last_date": "2026-07-31", "fast_transit": true, "max_senders_same_day": 3, "sync_in_days": 1, "max_recipients_same_day": 10, "sync_out_days": 2}

Маршруты: {"n_cycles": 472, "n_time_consistent_cycles": 45, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00010", "length": 2, "cycle_type": "reciprocal", "path": "100000000437046100→100000007639767100→100000000437046100", "min_edge_kzt": 27868.0, "total_kzt": 77868.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00011", "length": 2, "cycle_type": "reciprocal", "path": "100000000437046100→100000008293431100→100000000437046100", "min_edge_kzt": 15000.0, "total_kzt": 230000.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00012", "length": 2, "cycle_type": "reciprocal", "path": "100000000437046100→100000008686313100→100000000437046100", "min_edge_kzt": 29200.0, "total_kzt": 1134183.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}], "total": 485, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier", "split"], "examples": {"items": [{"anomaly_id": "A00010", "gid": "100000000437046100", "anomaly_type": "depth_outlier", "feature": "in_deg", "value": 9.0, "reference": 1.0, "ratio": 9.0, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00011", "gid": "100000000437046100", "anomaly_type": "depth_outlier", "feature": "in_tx", "value": 20.0, "reference": 1.0, "ratio": 20.0, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00012", "gid": "100000000437046100", "anomaly_type": "depth_outlier", "feature": "out_deg", "value": 42.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}], "total": 6, "truncated": true, "available": true}}

Что проверить дальше: ["Переводы ниже 5 000 ₸ по указанным узлам и парам", "Входящие переводы, включая межбанковские и пополнения наличными"]

---

GID: #100000008477350100
Роль: coordinator
Вход: 610,100 ₸; выход: 3,374,866 ₸.
Отправителей: 11; получателей: 39.
Соответствие роли: 0.8776; приоритет: 0.955098.
Основание: Связующий узел: посредничество ≥ p99, 4 других кластеров, 8 хабов; вход 610,1 тыс ₸, выход 3,4 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "coordinator", "role_score": 0.8776, "priority_score": 0.955098, "priority_rank": 7, "rule_id": "R_COORD", "rule_text": "betweenness >= 0.0019892319141409562; n_nbr_clusters >= 2; max(up_hubs, down_hubs) >= 2", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 11, "out_deg": 39, "in_kzt": 610100.0, "out_kzt": 3374866.0, "pass_through": 5.531660383543682, "depth": 2, "betweenness": 0.0025171940682580047, "n_nbr_clusters": 4, "up_hubs": 7, "down_hubs": 8}, "alternatives": [{"role": "distributor", "rule_id": "R_DIST", "strength": 3.9}, {"role": "consolidator", "rule_id": "R_CONS", "strength": 2.2}]}

Связи: {"cluster_id": 0, "cluster": {"cluster_id": 0, "n_nodes": 277, "n_seed": 1, "sum_kzt_internal": 31227334.24, "top_gids": ["100000005910114100", "100000000437046100", "100000008477350100", "100000004400305100", "100000002398779100"], "hypothesis": "Смешанная структура: consolidator=9, distributor=3, transit=11, terminal=8, coordinator=9, peripheral=237; требуется ручной разбор", "hypothesis_rule": "H_MIXED", "role_counts": {"consolidator": 9, "distributor": 3, "transit": 11, "terminal": 8, "coordinator": 9, "peripheral": 237}, "component_ids": [0]}, "nearest_hub": "100000005910114100", "path": ["100000008477350100", "100000005910114100"], "n_nbr_clusters": 4}

Время: {"fast_matched_kzt": 441500.0, "fast_pass_share": 0.7236518603507621, "median_hold_days": 0, "burst_score": 2.0517241379310347, "burst": false, "active_days": 17, "first_date": "2026-07-01", "last_date": "2026-07-30", "fast_transit": true, "max_senders_same_day": 2, "sync_in_days": 0, "max_recipients_same_day": 6, "sync_out_days": 3}

Маршруты: {"n_cycles": 464, "n_time_consistent_cycles": 46, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00165", "length": 2, "cycle_type": "reciprocal", "path": "100000008086440100→100000008477350100→100000008086440100", "min_edge_kzt": 18900.0, "total_kzt": 218633.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00235", "length": 4, "cycle_type": "cycle", "path": "100000000437046100→100000004070318100→100000008477350100→100000007639767100→100000000437046100", "min_edge_kzt": 16305.0, "total_kzt": 181305.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00236", "length": 4, "cycle_type": "cycle", "path": "100000000437046100→100000004070318100→100000008477350100→100000008086440100→100000000437046100", "min_edge_kzt": 25000.0, "total_kzt": 356233.0, "has_seed": false, "time_consistent": false, "kind": "cycle"}], "total": 465, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier"], "examples": {"items": [{"anomaly_id": "A00162", "gid": "100000008477350100", "anomaly_type": "depth_outlier", "feature": "in_deg", "value": 11.0, "reference": 1.0, "ratio": 11.0, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}], "total": 1, "truncated": false, "available": true}}

Что проверить дальше: ["Входящие переводы, включая межбанковские и пополнения наличными"]

---

GID: #100000003115284100
Роль: consolidator
Вход: 2,160,500 ₸; выход: 517,000 ₸.
Отправителей: 8; получателей: 2.
Соответствие роли: 0.8; приоритет: 0.925897.
Основание: Признаки консолидации: 8 отправителей (порог 5); вход 2,2 млн ₸, выход 517,0 тыс ₸

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "consolidator", "role_score": 0.8, "priority_score": 0.925897, "priority_rank": 8, "rule_id": "R_CONS", "rule_text": "in_deg >= 5", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 8, "out_deg": 2, "in_kzt": 2160500.0, "out_kzt": 517000.0, "pass_through": 0.23929645915297384, "depth": 1, "betweenness": 0.00012780471914467138, "n_nbr_clusters": 4, "up_hubs": 7, "down_hubs": 0}, "alternatives": []}

Связи: {"cluster_id": 11, "cluster": {"cluster_id": 11, "n_nodes": 54, "n_seed": 1, "sum_kzt_internal": 6244622.0, "top_gids": ["100000003115284100", "100000008730846100", "100000007998965100", "100000003809101100", "100000000343175100"], "hypothesis": "Признаки веерного распределения от 100000000343175100 на 31 получателей", "hypothesis_rule": "H_FANOUT", "role_counts": {"consolidator": 3, "distributor": 2, "transit": 3, "terminal": 2, "coordinator": 0, "peripheral": 44}, "component_ids": [0]}, "nearest_hub": null, "path": [], "n_nbr_clusters": 4}

Время: {"fast_matched_kzt": 510000.0, "fast_pass_share": 0.23605646841009026, "median_hold_days": 0, "burst_score": 4.105263157894737, "burst": true, "active_days": 6, "first_date": "2026-07-01", "last_date": "2026-07-19", "fast_transit": false, "max_senders_same_day": 7, "sync_in_days": 1, "max_recipients_same_day": 2, "sync_out_days": 0}

Маршруты: {"n_cycles": 2, "n_time_consistent_cycles": 2, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00092", "length": 2, "cycle_type": "reciprocal", "path": "100000003115284100→100000003360542100→100000003115284100", "min_edge_kzt": 30500.0, "total_kzt": 337500.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00314", "length": 4, "cycle_type": "cycle", "path": "100000003115284100→100000003390036100→100000005873152100→100000003360542100→100000003115284100", "min_edge_kzt": 10000.0, "total_kzt": 260500.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"chain_id": "H00134", "a": "100000004390333100", "b": "100000003684369100", "c": "100000003115284100", "repeats": 2, "sum_ab": 100000.0, "sum_bc": 193000.0, "median_lag_days": 2.0, "first_date": "2026-07-17", "last_date": "2026-07-19", "kind": "chain"}], "total": 5, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier"], "examples": {"items": [{"anomaly_id": "A00059", "gid": "100000003115284100", "anomaly_type": "depth_outlier", "feature": "in_deg", "value": 8.0, "reference": 1.0, "ratio": 8.0, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00060", "gid": "100000003115284100", "anomaly_type": "depth_outlier", "feature": "in_kzt", "value": 2160500.0, "reference": 65000.0, "ratio": 33.238461538461536, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}], "total": 2, "truncated": false, "available": true}}

Что проверить дальше: ["Проверить полноту контрагентов и операций за пределами среза."]

---

GID: #100000004015047100
Роль: consolidator
Вход: 919,104 ₸; выход: 69,195 ₸.
Отправителей: 9; получателей: 1.
Соответствие роли: 0.9; приоритет: 0.924475.
Основание: Признаки консолидации: 9 отправителей (порог 5); вход 919,1 тыс ₸, выход 69,2 тыс ₸

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "consolidator", "role_score": 0.9, "priority_score": 0.924475, "priority_rank": 9, "rule_id": "R_CONS", "rule_text": "in_deg >= 5", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 9, "out_deg": 1, "in_kzt": 919104.0, "out_kzt": 69195.0, "pass_through": 0.07528527783580531, "depth": 1, "betweenness": 2.2885961335208597e-05, "n_nbr_clusters": 4, "up_hubs": 3, "down_hubs": 1}, "alternatives": []}

Связи: {"cluster_id": 8, "cluster": {"cluster_id": 8, "n_nodes": 61, "n_seed": 3, "sum_kzt_internal": 8902320.0, "top_gids": ["100000004015047100", "100000008748408100", "100000006788200100", "100000002870463100", "100000003111305100"], "hypothesis": "Признаки сбора средств от 3 seed с концентрацией у 100000004015047100", "hypothesis_rule": "H_COLLECT", "role_counts": {"consolidator": 2, "distributor": 1, "transit": 4, "terminal": 4, "coordinator": 0, "peripheral": 50}, "component_ids": [0]}, "nearest_hub": "100000001616816100", "path": ["100000004015047100", "100000001616816100"], "n_nbr_clusters": 4}

Время: {"fast_matched_kzt": 44032.0, "fast_pass_share": 0.04790752733096581, "median_hold_days": 0, "burst_score": 2.2399999999999998, "burst": false, "active_days": 14, "first_date": "2026-07-01", "last_date": "2026-07-23", "fast_transit": false, "max_senders_same_day": 2, "sync_in_days": 0, "max_recipients_same_day": 1, "sync_out_days": 0}

Маршруты: {"n_cycles": 1, "n_time_consistent_cycles": 1, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00041", "length": 2, "cycle_type": "reciprocal", "path": "100000001616816100→100000004015047100→100000001616816100", "min_edge_kzt": 69195.0, "total_kzt": 179695.0, "has_seed": true, "time_consistent": true, "kind": "cycle"}, {"chain_id": "H00065", "a": "100000004015047100", "b": "100000001616816100", "c": "100000004015047100", "repeats": 3, "sum_ab": 69195.0, "sum_bc": 110500.0, "median_lag_days": 1.0, "first_date": "2026-07-01", "last_date": "2026-07-04", "kind": "chain"}, {"chain_id": "H00151", "a": "100000001616816100", "b": "100000004015047100", "c": "100000001616816100", "repeats": 2, "sum_ab": 110500.0, "sum_bc": 69195.0, "median_lag_days": 0.0, "first_date": "2026-07-02", "last_date": "2026-07-03", "kind": "chain"}], "total": 3, "truncated": false, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier"], "examples": {"items": [{"anomaly_id": "A00078", "gid": "100000004015047100", "anomaly_type": "depth_outlier", "feature": "in_deg", "value": 9.0, "reference": 1.0, "ratio": 9.0, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00079", "gid": "100000004015047100", "anomaly_type": "depth_outlier", "feature": "in_tx", "value": 18.0, "reference": 1.0, "ratio": 18.0, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}], "total": 2, "truncated": false, "available": true}}

Что проверить дальше: ["Проверить полноту контрагентов и операций за пределами среза."]

---

GID: #100000004400305100
Роль: coordinator
Вход: 222,800 ₸; выход: 5,830,181 ₸.
Отправителей: 7; получателей: 82.
Соответствие роли: 0.8853; приоритет: 0.92307.
Основание: Связующий узел: посредничество ≥ p99, 9 других кластеров, 16 хабов; вход 222,8 тыс ₸, выход 5,8 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "coordinator", "role_score": 0.8853, "priority_score": 0.92307, "priority_rank": 10, "rule_id": "R_COORD", "rule_text": "betweenness >= 0.0019892319141409562; n_nbr_clusters >= 2; max(up_hubs, down_hubs) >= 2", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 7, "out_deg": 82, "in_kzt": 222800.0, "out_kzt": 5830181.0, "pass_through": 26.167778276481148, "depth": 2, "betweenness": 0.002609149922720262, "n_nbr_clusters": 9, "up_hubs": 6, "down_hubs": 16}, "alternatives": [{"role": "distributor", "rule_id": "R_DIST", "strength": 8.2}, {"role": "consolidator", "rule_id": "R_CONS", "strength": 1.4}]}

Связи: {"cluster_id": 0, "cluster": {"cluster_id": 0, "n_nodes": 277, "n_seed": 1, "sum_kzt_internal": 31227334.24, "top_gids": ["100000005910114100", "100000000437046100", "100000008477350100", "100000004400305100", "100000002398779100"], "hypothesis": "Смешанная структура: consolidator=9, distributor=3, transit=11, terminal=8, coordinator=9, peripheral=237; требуется ручной разбор", "hypothesis_rule": "H_MIXED", "role_counts": {"consolidator": 9, "distributor": 3, "transit": 11, "terminal": 8, "coordinator": 9, "peripheral": 237}, "component_ids": [0]}, "nearest_hub": "100000005910114100", "path": ["100000004400305100", "100000005910114100"], "n_nbr_clusters": 9}

Время: {"fast_matched_kzt": 222800.0, "fast_pass_share": 1.0, "median_hold_days": 0, "burst_score": 2.2, "burst": false, "active_days": 22, "first_date": "2026-07-03", "last_date": "2026-07-29", "fast_transit": true, "max_senders_same_day": 2, "sync_in_days": 0, "max_recipients_same_day": 9, "sync_out_days": 12}

Маршруты: {"n_cycles": 545, "n_time_consistent_cycles": 34, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00094", "length": 2, "cycle_type": "reciprocal", "path": "100000003213473100→100000004400305100→100000003213473100", "min_edge_kzt": 9000.0, "total_kzt": 66500.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00116", "length": 2, "cycle_type": "reciprocal", "path": "100000004070318100→100000004400305100→100000004070318100", "min_edge_kzt": 19800.0, "total_kzt": 42800.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00226", "length": 4, "cycle_type": "cycle", "path": "100000000437046100→100000004070318100→100000004400305100→100000004390333100→100000000437046100", "min_edge_kzt": 18807.0, "total_kzt": 228607.0, "has_seed": false, "time_consistent": false, "kind": "cycle"}], "total": 550, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier", "split"], "examples": {"items": [{"anomaly_id": "A00091", "gid": "100000004400305100", "anomaly_type": "depth_outlier", "feature": "out_deg", "value": 82.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00092", "gid": "100000004400305100", "anomaly_type": "depth_outlier", "feature": "out_kzt", "value": 5830181.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00093", "gid": "100000004400305100", "anomaly_type": "depth_outlier", "feature": "out_tx", "value": 101.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}], "total": 4, "truncated": true, "available": true}}

Что проверить дальше: ["Переводы ниже 5 000 ₸ по указанным узлам и парам", "Входящие переводы, включая межбанковские и пополнения наличными"]

---

GID: #100000005933757100
Роль: distributor
Вход: 1,246,000 ₸; выход: 3,002,628 ₸.
Отправителей: 4; получателей: 34.
Соответствие роли: 1.0; приоритет: 0.920267.
Основание: Веерное распределение: 34 получателей (порог 10); вход 1,2 млн ₸, выход 3,0 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "distributor", "role_score": 1.0, "priority_score": 0.920267, "priority_rank": 11, "rule_id": "R_DIST", "rule_text": "out_deg >= 10", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 4, "out_deg": 34, "in_kzt": 1246000.0, "out_kzt": 3002628.0, "pass_through": 2.409813804173355, "depth": 2, "betweenness": 0.0038927878243158664, "n_nbr_clusters": 9, "up_hubs": 0, "down_hubs": 1}, "alternatives": []}

Связи: {"cluster_id": 14, "cluster": {"cluster_id": 14, "n_nodes": 44, "n_seed": 0, "sum_kzt_internal": 10215968.84, "top_gids": ["100000005933757100", "100000002963189100", "100000004159526100", "100000001937767100", "100000001073568100"], "hypothesis": "Фрагмент без seed на 1-м колене; назначение не определено", "hypothesis_rule": "H_NOSEED", "role_counts": {"consolidator": 0, "distributor": 1, "transit": 0, "terminal": 4, "coordinator": 0, "peripheral": 39}, "component_ids": [0]}, "nearest_hub": "100000004403675100", "path": ["100000005933757100", "100000004403675100"], "n_nbr_clusters": 9}

Время: {"fast_matched_kzt": 1246000.0, "fast_pass_share": 1.0, "median_hold_days": 1, "burst_score": 2.8846153846153846, "burst": false, "active_days": 15, "first_date": "2026-07-01", "last_date": "2026-07-21", "fast_transit": true, "max_senders_same_day": 2, "sync_in_days": 0, "max_recipients_same_day": 8, "sync_out_days": 3}

Маршруты: {"n_cycles": 3, "n_time_consistent_cycles": 2, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00085", "length": 2, "cycle_type": "reciprocal", "path": "100000002963189100→100000005933757100→100000002963189100", "min_edge_kzt": 490000.0, "total_kzt": 1640000.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00137", "length": 2, "cycle_type": "reciprocal", "path": "100000004569484100→100000005933757100→100000004569484100", "min_edge_kzt": 32607.0, "total_kzt": 71607.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00366", "length": 4, "cycle_type": "cycle", "path": "100000004569484100→100000005933757100→100000008104567100→100000005704413100→100000004569484100", "min_edge_kzt": 20000.0, "total_kzt": 145255.0, "has_seed": false, "time_consistent": false, "kind": "cycle"}], "total": 7, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["split"], "examples": {"items": [{"anomaly_id": "A00133", "gid": "100000005933757100", "anomaly_type": "split_pair", "feature": "n_tx_window", "value": 3.0, "reference": 0.0, "ratio": null, "counterparty_gid": "100000004500444100", "description": "Похожие суммы в коротком окне; дробление ниже 5 000 ₸ в данных не видно."}], "total": 1, "truncated": false, "available": true}}

Что проверить дальше: ["Переводы ниже 5 000 ₸ по указанным узлам и парам", "Входящие переводы, включая межбанковские и пополнения наличными"]

---

GID: #100000002398779100
Роль: consolidator
Вход: 1,095,690 ₸; выход: 66,000 ₸.
Отправителей: 13; получателей: 1.
Соответствие роли: 1.0; приоритет: 0.909034.
Основание: Признаки консолидации: 13 отправителей (порог 5); вход 1,1 млн ₸, выход 66,0 тыс ₸

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "consolidator", "role_score": 1.0, "priority_score": 0.909034, "priority_rank": 12, "rule_id": "R_CONS", "rule_text": "in_deg >= 5", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 13, "out_deg": 1, "in_kzt": 1095690.0, "out_kzt": 66000.0, "pass_through": 0.06023601566136407, "depth": 2, "betweenness": 1.2780471914467137e-05, "n_nbr_clusters": 2, "up_hubs": 7, "down_hubs": 0}, "alternatives": []}

Связи: {"cluster_id": 0, "cluster": {"cluster_id": 0, "n_nodes": 277, "n_seed": 1, "sum_kzt_internal": 31227334.24, "top_gids": ["100000005910114100", "100000000437046100", "100000008477350100", "100000004400305100", "100000002398779100"], "hypothesis": "Смешанная структура: consolidator=9, distributor=3, transit=11, terminal=8, coordinator=9, peripheral=237; требуется ручной разбор", "hypothesis_rule": "H_MIXED", "role_counts": {"consolidator": 9, "distributor": 3, "transit": 11, "terminal": 8, "coordinator": 9, "peripheral": 237}, "component_ids": [0]}, "nearest_hub": null, "path": [], "n_nbr_clusters": 2}

Время: {"fast_matched_kzt": 66000.0, "fast_pass_share": 0.06023601566136407, "median_hold_days": 2, "burst_score": 2.096774193548387, "burst": false, "active_days": 5, "first_date": "2026-07-06", "last_date": "2026-07-10", "fast_transit": false, "max_senders_same_day": 7, "sync_in_days": 3, "max_recipients_same_day": 1, "sync_out_days": 0}

Маршруты: {"n_cycles": 0, "n_time_consistent_cycles": 0, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"chain_id": "H00067", "a": "100000004070318100", "b": "100000002398779100", "c": "100000008576243100", "repeats": 3, "sum_ab": 61568.0, "sum_bc": 66000.0, "median_lag_days": 1.0, "first_date": "2026-07-07", "last_date": "2026-07-10", "kind": "chain"}, {"chain_id": "H00068", "a": "100000004400305100", "b": "100000002645993100", "c": "100000002398779100", "repeats": 3, "sum_ab": 35650.0, "sum_bc": 54150.0, "median_lag_days": 0.0, "first_date": "2026-07-07", "last_date": "2026-07-07", "kind": "chain"}, {"chain_id": "H00103", "a": "100000005910114100", "b": "100000004486525100", "c": "100000002398779100", "repeats": 2, "sum_ab": 195047.0, "sum_bc": 254955.0, "median_lag_days": 2.0, "first_date": "2026-07-04", "last_date": "2026-07-06", "kind": "chain"}], "total": 9, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier"], "examples": {"items": [{"anomaly_id": "A00037", "gid": "100000002398779100", "anomaly_type": "depth_outlier", "feature": "in_deg", "value": 13.0, "reference": 1.0, "ratio": 13.0, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00038", "gid": "100000002398779100", "anomaly_type": "depth_outlier", "feature": "in_tx", "value": 28.0, "reference": 1.0, "ratio": 28.0, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}], "total": 2, "truncated": false, "available": true}}

Что проверить дальше: ["Проверить полноту контрагентов и операций за пределами среза."]

---

GID: #100000004070318100
Роль: coordinator
Вход: 207,246.55 ₸; выход: 551,860 ₸.
Отправителей: 4; получателей: 19.
Соответствие роли: 0.8404; приоритет: 0.907771.
Основание: Связующий узел: посредничество ≥ p99, 8 других кластеров, 12 хабов; вход 207,2 тыс ₸, выход 551,9 тыс ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "coordinator", "role_score": 0.8404, "priority_score": 0.907771, "priority_rank": 13, "rule_id": "R_COORD", "rule_text": "betweenness >= 0.0019892319141409562; n_nbr_clusters >= 2; max(up_hubs, down_hubs) >= 2", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 4, "out_deg": 19, "in_kzt": 207246.55, "out_kzt": 551860.0, "pass_through": 2.662818753798314, "depth": 1, "betweenness": 0.002073265129736242, "n_nbr_clusters": 8, "up_hubs": 4, "down_hubs": 12}, "alternatives": [{"role": "distributor", "rule_id": "R_DIST", "strength": 1.9}]}

Связи: {"cluster_id": 0, "cluster": {"cluster_id": 0, "n_nodes": 277, "n_seed": 1, "sum_kzt_internal": 31227334.24, "top_gids": ["100000005910114100", "100000000437046100", "100000008477350100", "100000004400305100", "100000002398779100"], "hypothesis": "Смешанная структура: consolidator=9, distributor=3, transit=11, terminal=8, coordinator=9, peripheral=237; требуется ручной разбор", "hypothesis_rule": "H_MIXED", "role_counts": {"consolidator": 9, "distributor": 3, "transit": 11, "terminal": 8, "coordinator": 9, "peripheral": 237}, "component_ids": [0]}, "nearest_hub": "100000008603629100", "path": ["100000004070318100", "100000008603629100"], "n_nbr_clusters": 8}

Время: {"fast_matched_kzt": 207246.55, "fast_pass_share": 1.0, "median_hold_days": 0, "burst_score": 2.7674418604651163, "burst": false, "active_days": 17, "first_date": "2026-07-01", "last_date": "2026-07-31", "fast_transit": true, "max_senders_same_day": 2, "sync_in_days": 0, "max_recipients_same_day": 4, "sync_out_days": 0}

Маршруты: {"n_cycles": 463, "n_time_consistent_cycles": 63, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00116", "length": 2, "cycle_type": "reciprocal", "path": "100000004070318100→100000004400305100→100000004070318100", "min_edge_kzt": 19800.0, "total_kzt": 42800.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00117", "length": 2, "cycle_type": "reciprocal", "path": "100000004070318100→100000006866783100→100000004070318100", "min_edge_kzt": 64725.0, "total_kzt": 149725.0, "has_seed": true, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00219", "length": 4, "cycle_type": "cycle", "path": "100000000089154100→100000000437046100→100000004070318100→100000006866783100→100000000089154100", "min_edge_kzt": 10000.0, "total_kzt": 217000.0, "has_seed": true, "time_consistent": true, "kind": "cycle"}], "total": 472, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier", "split"], "examples": {"items": [{"anomaly_id": "A00080", "gid": "100000004070318100", "anomaly_type": "depth_outlier", "feature": "out_deg", "value": 19.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00081", "gid": "100000004070318100", "anomaly_type": "depth_outlier", "feature": "out_tx", "value": 37.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00082", "gid": "100000004070318100", "anomaly_type": "split_pair", "feature": "n_tx_window", "value": 3.0, "reference": 0.128564869306645, "ratio": null, "counterparty_gid": "100000006866783100", "description": "Похожие суммы в коротком окне; дробление ниже 5 000 ₸ в данных не видно."}], "total": 3, "truncated": false, "available": true}}

Что проверить дальше: ["Переводы ниже 5 000 ₸ по указанным узлам и парам"]

---

GID: #100000003242289100
Роль: distributor
Вход: 550,791 ₸; выход: 2,377,741 ₸.
Отправителей: 3; получателей: 23.
Соответствие роли: 1.0; приоритет: 0.903971.
Основание: Веерное распределение: 23 получателей (порог 10); вход 550,8 тыс ₸, выход 2,4 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "distributor", "role_score": 1.0, "priority_score": 0.903971, "priority_rank": 14, "rule_id": "R_DIST", "rule_text": "out_deg >= 10", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 3, "out_deg": 23, "in_kzt": 550791.0, "out_kzt": 2377741.0, "pass_through": 4.316956885642648, "depth": 2, "betweenness": 0.0010013456094342644, "n_nbr_clusters": 4, "up_hubs": 2, "down_hubs": 2}, "alternatives": []}

Связи: {"cluster_id": 16, "cluster": {"cluster_id": 16, "n_nodes": 41, "n_seed": 0, "sum_kzt_internal": 5151924.19, "top_gids": ["100000003242289100", "100000008413748100", "100000008512552100", "100000006225798100", "100000003178549100"], "hypothesis": "Признаки веерного распределения от 100000003242289100 на 23 получателей", "hypothesis_rule": "H_FANOUT", "role_counts": {"consolidator": 0, "distributor": 2, "transit": 0, "terminal": 3, "coordinator": 0, "peripheral": 36}, "component_ids": [0]}, "nearest_hub": "100000008603629100", "path": ["100000003242289100", "100000004140487100", "100000008603629100"], "n_nbr_clusters": 4}

Время: {"fast_matched_kzt": 444065.0, "fast_pass_share": 0.8062314017476684, "median_hold_days": 2, "burst_score": 2.5, "burst": false, "active_days": 17, "first_date": "2026-07-02", "last_date": "2026-07-31", "fast_transit": true, "max_senders_same_day": 2, "sync_in_days": 0, "max_recipients_same_day": 4, "sync_out_days": 0}

Маршруты: {"n_cycles": 104, "n_time_consistent_cycles": 12, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00096", "length": 2, "cycle_type": "reciprocal", "path": "100000003242289100→100000008512552100→100000003242289100", "min_edge_kzt": 49000.0, "total_kzt": 517791.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00198", "length": 3, "cycle_type": "cycle", "path": "100000003242289100→100000008417359100→100000008512552100→100000003242289100", "min_edge_kzt": 20760.0, "total_kzt": 530361.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00298", "length": 4, "cycle_type": "cycle", "path": "100000002723538100→100000003242289100→100000004140487100→100000004400305100→100000002723538100", "min_edge_kzt": 15000.0, "total_kzt": 102510.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}], "total": 105, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": [], "examples": {"items": [], "total": 0, "truncated": false, "available": true}}

Что проверить дальше: ["Входящие переводы, включая межбанковские и пополнения наличными"]

---

GID: #100000004403675100
Роль: coordinator
Вход: 182,980 ₸; выход: 264,699 ₸.
Отправителей: 4; получателей: 5.
Соответствие роли: 0.8169; приоритет: 0.893404.
Основание: Связующий узел: посредничество ≥ p99, 4 других кластеров, 3 хабов; вход 183,0 тыс ₸, выход 264,7 тыс ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "coordinator", "role_score": 0.8169, "priority_score": 0.893404, "priority_rank": 15, "rule_id": "R_COORD", "rule_text": "betweenness >= 0.0019892319141409562; n_nbr_clusters >= 2; max(up_hubs, down_hubs) >= 2", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 4, "out_deg": 5, "in_kzt": 182980.0, "out_kzt": 264699.0, "pass_through": 1.4466007213903158, "depth": 1, "betweenness": 0.0027876735137262014, "n_nbr_clusters": 4, "up_hubs": 3, "down_hubs": 1}, "alternatives": []}

Связи: {"cluster_id": 19, "cluster": {"cluster_id": 19, "n_nodes": 26, "n_seed": 14, "sum_kzt_internal": 2289450.0, "top_gids": ["100000004403675100", "100000005382566100", "100000003823811100", "100000008254069100", "100000004744306100"], "hypothesis": "Признаки сбора средств от 14 seed с концентрацией у 100000004403675100", "hypothesis_rule": "H_COLLECT", "role_counts": {"consolidator": 1, "distributor": 0, "transit": 0, "terminal": 1, "coordinator": 1, "peripheral": 23}, "component_ids": [0]}, "nearest_hub": "100000000331309100", "path": ["100000004403675100", "100000000331309100"], "n_nbr_clusters": 4}

Время: {"fast_matched_kzt": 74693.0, "fast_pass_share": 0.4082030823040769, "median_hold_days": 1, "burst_score": 2.857142857142857, "burst": false, "active_days": 8, "first_date": "2026-07-01", "last_date": "2026-07-20", "fast_transit": false, "max_senders_same_day": 1, "sync_in_days": 0, "max_recipients_same_day": 2, "sync_out_days": 0}

Маршруты: {"n_cycles": 10, "n_time_consistent_cycles": 1, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00111", "length": 2, "cycle_type": "reciprocal", "path": "100000003988112100→100000004403675100→100000003988112100", "min_edge_kzt": 64000.0, "total_kzt": 156000.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00224", "length": 4, "cycle_type": "cycle", "path": "100000000331309100→100000008686313100→100000006866783100→100000004403675100→100000000331309100", "min_edge_kzt": 47187.0, "total_kzt": 527764.0, "has_seed": true, "time_consistent": false, "kind": "cycle"}, {"cycle_id": "C00520", "length": 6, "cycle_type": "cycle", "path": "100000000331309100→100000004746397100→100000002957787100→100000008632060100→100000006866783100→100000004403675100→100000000331309100", "min_edge_kzt": 6000.0, "total_kzt": 359642.0, "has_seed": true, "time_consistent": false, "kind": "cycle"}], "total": 12, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": [], "examples": {"items": [], "total": 0, "truncated": false, "available": true}}

Что проверить дальше: ["Проверить полноту контрагентов и операций за пределами среза."]

---

GID: #100000008489922100
Роль: distributor
Вход: 262,010 ₸; выход: 3,789,900 ₸.
Отправителей: 3; получателей: 36.
Соответствие роли: 1.0; приоритет: 0.891495.
Основание: Веерное распределение: 36 получателей (порог 10); вход 262,0 тыс ₸, выход 3,8 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "distributor", "role_score": 1.0, "priority_score": 0.891495, "priority_rank": 16, "rule_id": "R_DIST", "rule_text": "out_deg >= 10", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 3, "out_deg": 36, "in_kzt": 262010.0, "out_kzt": 3789900.0, "pass_through": 14.464715087210411, "depth": 3, "betweenness": 0.0008721882963004521, "n_nbr_clusters": 5, "up_hubs": 2, "down_hubs": 4}, "alternatives": []}

Связи: {"cluster_id": 2, "cluster": {"cluster_id": 2, "n_nodes": 158, "n_seed": 1, "sum_kzt_internal": 32434270.59, "top_gids": ["100000008489922100", "100000008547948100", "100000008710791100", "100000008547844100", "100000008517538100"], "hypothesis": "Признаки веерного распределения от 100000008489922100 на 36 получателей", "hypothesis_rule": "H_FANOUT", "role_counts": {"consolidator": 2, "distributor": 10, "transit": 3, "terminal": 22, "coordinator": 0, "peripheral": 121}, "component_ids": [0]}, "nearest_hub": null, "path": [], "n_nbr_clusters": 5}

Время: {"fast_matched_kzt": 233000.0, "fast_pass_share": 0.8892790351513301, "median_hold_days": 1, "burst_score": 2.934782608695652, "burst": false, "active_days": 15, "first_date": "2026-07-13", "last_date": "2026-07-31", "fast_transit": true, "max_senders_same_day": 2, "sync_in_days": 0, "max_recipients_same_day": 7, "sync_out_days": 3}

Маршруты: {"n_cycles": 6, "n_time_consistent_cycles": 1, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00171", "length": 2, "cycle_type": "reciprocal", "path": "100000008489922100→100000008547948100→100000008489922100", "min_edge_kzt": 30000.0, "total_kzt": 117000.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00387", "length": 4, "cycle_type": "cycle", "path": "100000008489922100→100000008710843100→100000008547844100→100000008547948100→100000008489922100", "min_edge_kzt": 18200.0, "total_kzt": 235200.0, "has_seed": false, "time_consistent": false, "kind": "cycle"}, {"cycle_id": "C00466", "length": 5, "cycle_type": "cycle", "path": "100000008465789100→100000008466579100→100000008489922100→100000008547948100→100000008547844100→100000008465789100", "min_edge_kzt": 30000.0, "total_kzt": 313099.0, "has_seed": false, "time_consistent": false, "kind": "cycle"}], "total": 6, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier"], "examples": {"items": [{"anomaly_id": "A00163", "gid": "100000008489922100", "anomaly_type": "depth_outlier", "feature": "out_deg", "value": 36.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00164", "gid": "100000008489922100", "anomaly_type": "depth_outlier", "feature": "out_kzt", "value": 3789900.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}, {"anomaly_id": "A00165", "gid": "100000008489922100", "anomaly_type": "depth_outlier", "feature": "out_tx", "value": 41.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}], "total": 3, "truncated": false, "available": true}}

Что проверить дальше: ["Входящие переводы, включая межбанковские и пополнения наличными"]

---

GID: #100000004156082100
Роль: distributor
Вход: 377,366.11 ₸; выход: 2,319,556 ₸.
Отправителей: 5; получателей: 26.
Соответствие роли: 1.0; приоритет: 0.890966.
Основание: Веерное распределение: 26 получателей (порог 10); вход 377,4 тыс ₸, выход 2,3 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "distributor", "role_score": 1.0, "priority_score": 0.890966, "priority_rank": 17, "rule_id": "R_DIST", "rule_text": "out_deg >= 10", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 5, "out_deg": 26, "in_kzt": 377366.11, "out_kzt": 2319556.0, "pass_through": 6.146699288921308, "depth": 1, "betweenness": 0.0020400351394137825, "n_nbr_clusters": 3, "up_hubs": 0, "down_hubs": 0}, "alternatives": [{"role": "consolidator", "rule_id": "R_CONS", "strength": 1.0}]}

Связи: {"cluster_id": 15, "cluster": {"cluster_id": 15, "n_nodes": 41, "n_seed": 3, "sum_kzt_internal": 4888834.28, "top_gids": ["100000004156082100", "100000005339662100", "100000004820260100", "100000008188026100", "100000001987030100"], "hypothesis": "Смешанная структура: distributor=1, transit=3, terminal=2, peripheral=35; требуется ручной разбор", "hypothesis_rule": "H_MIXED", "role_counts": {"consolidator": 0, "distributor": 1, "transit": 3, "terminal": 2, "coordinator": 0, "peripheral": 35}, "component_ids": [0]}, "nearest_hub": "100000004188160100", "path": ["100000004156082100", "100000004188160100"], "n_nbr_clusters": 3}

Время: {"fast_matched_kzt": 377366.11, "fast_pass_share": 1.0, "median_hold_days": 0, "burst_score": 1.7499999999999998, "burst": false, "active_days": 7, "first_date": "2026-07-23", "last_date": "2026-07-31", "fast_transit": true, "max_senders_same_day": 2, "sync_in_days": 0, "max_recipients_same_day": 7, "sync_out_days": 3}

Маршруты: {"n_cycles": 11, "n_time_consistent_cycles": 6, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00122", "length": 2, "cycle_type": "reciprocal", "path": "100000004156082100→100000005287097100→100000004156082100", "min_edge_kzt": 16450.0, "total_kzt": 66950.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00259", "length": 4, "cycle_type": "cycle", "path": "100000001049200100→100000004156082100→100000004188160100→100000003016635100→100000001049200100", "min_edge_kzt": 6014.0, "total_kzt": 53614.0, "has_seed": true, "time_consistent": false, "kind": "cycle"}, {"cycle_id": "C00260", "length": 4, "cycle_type": "cycle", "path": "100000001049200100→100000004156082100→100000005287097100→100000003016635100→100000001049200100", "min_edge_kzt": 6014.0, "total_kzt": 435964.0, "has_seed": true, "time_consistent": true, "kind": "cycle"}], "total": 12, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier"], "examples": {"items": [{"anomaly_id": "A00086", "gid": "100000004156082100", "anomaly_type": "depth_outlier", "feature": "out_deg", "value": 26.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}], "total": 1, "truncated": false, "available": true}}

Что проверить дальше: ["Входящие переводы, включая межбанковские и пополнения наличными"]

---

GID: #100000004351795100
Роль: coordinator
Вход: 118,333 ₸; выход: 1,715,161 ₸.
Отправителей: 3; получателей: 14.
Соответствие роли: 0.8701; приоритет: 0.887304.
Основание: Связующий узел: посредничество ≥ p99, 5 других кластеров, 5 хабов; вход 118,3 тыс ₸, выход 1,7 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "coordinator", "role_score": 0.8701, "priority_score": 0.887304, "priority_rank": 18, "rule_id": "R_COORD", "rule_text": "betweenness >= 0.0019892319141409562; n_nbr_clusters >= 2; max(up_hubs, down_hubs) >= 2", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 3, "out_deg": 14, "in_kzt": 118333.0, "out_kzt": 1715161.0, "pass_through": 14.494359139039828, "depth": 1, "betweenness": 0.002428521604147366, "n_nbr_clusters": 5, "up_hubs": 3, "down_hubs": 5}, "alternatives": [{"role": "distributor", "rule_id": "R_DIST", "strength": 1.4}]}

Связи: {"cluster_id": 0, "cluster": {"cluster_id": 0, "n_nodes": 277, "n_seed": 1, "sum_kzt_internal": 31227334.24, "top_gids": ["100000005910114100", "100000000437046100", "100000008477350100", "100000004400305100", "100000002398779100"], "hypothesis": "Смешанная структура: consolidator=9, distributor=3, transit=11, terminal=8, coordinator=9, peripheral=237; требуется ручной разбор", "hypothesis_rule": "H_MIXED", "role_counts": {"consolidator": 9, "distributor": 3, "transit": 11, "terminal": 8, "coordinator": 9, "peripheral": 237}, "component_ids": [0]}, "nearest_hub": "100000008603629100", "path": ["100000004351795100", "100000008603629100"], "n_nbr_clusters": 5}

Время: {"fast_matched_kzt": 118333.0, "fast_pass_share": 1.0, "median_hold_days": 2, "burst_score": 2.375, "burst": false, "active_days": 19, "first_date": "2026-07-01", "last_date": "2026-07-30", "fast_transit": true, "max_senders_same_day": 1, "sync_in_days": 0, "max_recipients_same_day": 5, "sync_out_days": 1}

Маршруты: {"n_cycles": 206, "n_time_consistent_cycles": 22, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00127", "length": 2, "cycle_type": "reciprocal", "path": "100000004351795100→100000008603629100→100000004351795100", "min_edge_kzt": 22418.0, "total_kzt": 99418.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00178", "length": 3, "cycle_type": "cycle", "path": "100000000437046100→100000008603629100→100000004351795100→100000000437046100", "min_edge_kzt": 5000.0, "total_kzt": 569418.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00229", "length": 4, "cycle_type": "cycle", "path": "100000000437046100→100000004070318100→100000006866783100→100000004351795100→100000000437046100", "min_edge_kzt": 66404.0, "total_kzt": 783404.0, "has_seed": true, "time_consistent": false, "kind": "cycle"}], "total": 212, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["depth_outlier"], "examples": {"items": [{"anomaly_id": "A00090", "gid": "100000004351795100", "anomaly_type": "depth_outlier", "feature": "out_tx", "value": 37.0, "reference": 0.0, "ratio": null, "counterparty_gid": null, "description": "Выше сверстников по колену и глобального порога; при нулевой медиане отношение не определено."}], "total": 1, "truncated": false, "available": true}}

Что проверить дальше: ["Входящие переводы, включая межбанковские и пополнения наличными"]

---

GID: #100000008547948100
Роль: distributor
Вход: 212,665 ₸; выход: 5,185,600 ₸.
Отправителей: 6; получателей: 26.
Соответствие роли: 1.0; приоритет: 0.88314.
Основание: Веерное распределение: 26 получателей (порог 10); вход 212,7 тыс ₸, выход 5,2 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "distributor", "role_score": 1.0, "priority_score": 0.88314, "priority_rank": 19, "rule_id": "R_DIST", "rule_text": "out_deg >= 10", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 6, "out_deg": 26, "in_kzt": 212665.0, "out_kzt": 5185600.0, "pass_through": 24.383890155878966, "depth": 2, "betweenness": 0.0011322141374262575, "n_nbr_clusters": 5, "up_hubs": 5, "down_hubs": 4}, "alternatives": [{"role": "consolidator", "rule_id": "R_CONS", "strength": 1.2}]}

Связи: {"cluster_id": 2, "cluster": {"cluster_id": 2, "n_nodes": 158, "n_seed": 1, "sum_kzt_internal": 32434270.59, "top_gids": ["100000008489922100", "100000008547948100", "100000008710791100", "100000008547844100", "100000008517538100"], "hypothesis": "Признаки веерного распределения от 100000008489922100 на 36 получателей", "hypothesis_rule": "H_FANOUT", "role_counts": {"consolidator": 2, "distributor": 10, "transit": 3, "terminal": 22, "coordinator": 0, "peripheral": 121}, "component_ids": [0]}, "nearest_hub": "100000008165763100", "path": ["100000008547948100", "100000008547844100", "100000008465789100", "100000008223661100", "100000008165763100"], "n_nbr_clusters": 5}

Время: {"fast_matched_kzt": 212665.0, "fast_pass_share": 1.0, "median_hold_days": 0, "burst_score": 2.0526315789473686, "burst": false, "active_days": 13, "first_date": "2026-07-16", "last_date": "2026-07-31", "fast_transit": true, "max_senders_same_day": 4, "sync_in_days": 1, "max_recipients_same_day": 4, "sync_out_days": 0}

Маршруты: {"n_cycles": 8, "n_time_consistent_cycles": 3, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00171", "length": 2, "cycle_type": "reciprocal", "path": "100000008489922100→100000008547948100→100000008489922100", "min_edge_kzt": 30000.0, "total_kzt": 117000.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00173", "length": 2, "cycle_type": "reciprocal", "path": "100000008547844100→100000008547948100→100000008547844100", "min_edge_kzt": 61000.0, "total_kzt": 161000.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00217", "length": 3, "cycle_type": "cycle", "path": "100000008465789100→100000008547948100→100000008547844100→100000008465789100", "min_edge_kzt": 20000.0, "total_kzt": 150099.0, "has_seed": false, "time_consistent": true, "kind": "cycle"}], "total": 8, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": [], "examples": {"items": [], "total": 0, "truncated": false, "available": true}}

Что проверить дальше: ["Входящие переводы, включая межбанковские и пополнения наличными"]

---

GID: #100000002957787100
Роль: coordinator
Вход: 84,956 ₸; выход: 1,276,153.96 ₸.
Отправителей: 4; получателей: 34.
Соответствие роли: 0.9167; приоритет: 0.881291.
Основание: Связующий узел: посредничество ≥ p99, 8 других кластеров, 3 хабов; вход 85,0 тыс ₸, выход 1,3 млн ₸; отдаёт больше наблюдаемого входа — вероятны внешние поступления

Ограничения: анализ наблюдаемого среза, а не всей финансовой деятельности. Роли — гипотезы; внешние поступления и продолжение цепочек могут отсутствовать в данных.

Правило и альтернативы: {"role": "coordinator", "role_score": 0.9167, "priority_score": 0.881291, "priority_rank": 20, "rule_id": "R_COORD", "rule_text": "betweenness >= 0.0019892319141409562; n_nbr_clusters >= 2; max(up_hubs, down_hubs) >= 2", "thresholds": {"cons_min_in_deg": 5, "dist_min_out_deg": 10, "transit_low": 0.8, "transit_high": 1.2, "term_min_in_kzt": 300000, "coord_bc_threshold": 0.0019892319141409562, "coord_min_nbr_clusters": 2, "coord_min_hubs": 2, "boundary_depth": 4}, "values": {"in_deg": 4, "out_deg": 34, "in_kzt": 84956.0, "out_kzt": 1276153.96, "pass_through": 15.02135175855737, "depth": 2, "betweenness": 0.004276645426207853, "n_nbr_clusters": 8, "up_hubs": 2, "down_hubs": 3}, "alternatives": [{"role": "distributor", "rule_id": "R_DIST", "strength": 3.4}]}

Связи: {"cluster_id": 0, "cluster": {"cluster_id": 0, "n_nodes": 277, "n_seed": 1, "sum_kzt_internal": 31227334.24, "top_gids": ["100000005910114100", "100000000437046100", "100000008477350100", "100000004400305100", "100000002398779100"], "hypothesis": "Смешанная структура: consolidator=9, distributor=3, transit=11, terminal=8, coordinator=9, peripheral=237; требуется ручной разбор", "hypothesis_rule": "H_MIXED", "role_counts": {"consolidator": 9, "distributor": 3, "transit": 11, "terminal": 8, "coordinator": 9, "peripheral": 237}, "component_ids": [0]}, "nearest_hub": "100000004071080100", "path": ["100000002957787100", "100000004071080100"], "n_nbr_clusters": 8}

Время: {"fast_matched_kzt": 84956.0, "fast_pass_share": 1.0, "median_hold_days": 0, "burst_score": 2.0, "burst": false, "active_days": 8, "first_date": "2026-07-01", "last_date": "2026-07-08", "fast_transit": true, "max_senders_same_day": 2, "sync_in_days": 0, "max_recipients_same_day": 9, "sync_out_days": 3}

Маршруты: {"n_cycles": 84, "n_time_consistent_cycles": 1, "examples": {"limitation": "Даты не доказывают движение одних и тех же средств.", "items": [{"cycle_id": "C00084", "length": 2, "cycle_type": "reciprocal", "path": "100000002957787100→100000005268319100→100000002957787100", "min_edge_kzt": 19712.8, "total_kzt": 43712.8, "has_seed": false, "time_consistent": true, "kind": "cycle"}, {"cycle_id": "C00225", "length": 4, "cycle_type": "cycle", "path": "100000000437046100→100000004070318100→100000002957787100→100000008632060100→100000000437046100", "min_edge_kzt": 6000.0, "total_kzt": 171100.0, "has_seed": false, "time_consistent": false, "kind": "cycle"}, {"cycle_id": "C00296", "length": 4, "cycle_type": "cycle", "path": "100000002645993100→100000008413748100→100000004070318100→100000002957787100→100000002645993100", "min_edge_kzt": 7600.0, "total_kzt": 64601.55, "has_seed": false, "time_consistent": false, "kind": "cycle"}], "total": 90, "truncated": true, "available": true}}

Аномалии: {"anomaly_flags": ["split"], "examples": {"items": [{"anomaly_id": "A00112", "gid": "100000005268319100", "anomaly_type": "split_pair", "feature": "n_tx_window", "value": 3.0, "reference": 0.10206207261596574, "ratio": null, "counterparty_gid": "100000002957787100", "description": "Похожие суммы в коротком окне; дробление ниже 5 000 ₸ в данных не видно."}], "total": 1, "truncated": false, "available": true}}

Что проверить дальше: ["Переводы ниже 5 000 ₸ по указанным узлам и парам"]