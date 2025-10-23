import streamlit as st
import pandas as pd
import re
from datetime import datetime, timedelta
import hashlib
import json
import os
from pathlib import Path
import time
from io import BytesIO
import pickle

# ページ設定
st.set_page_config(
    page_title="AIテレアポ管理システム セールス",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 白背景で見やすい青ベースのカスタムCSS
st.markdown("""
<style>
    /* 全体の背景を白に */
    .stApp {
        background-color: #ffffff;
        color: #333333;
    }
    
    /* メインコンテンツエリア */
    .main .block-container {
        background-color: #ffffff;
        padding: 2rem;
        max-width: 1200px;
    }
    
    /* サイドバー */
    .css-1d391kg {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    /* ヘッダー */
    .main-header {
        font-size: 2.5rem;
        color: #1e40af;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        padding: 1rem 0;
        border-bottom: 3px solid #3b82f6;
    }
    
    /* ジョブカード - 清潔感のあるデザイン */
    .job-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 2px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
        border-color: #3b82f6;
    }
    
    .job-card-header {
        font-size: 1.3rem;
        font-weight: bold;
        color: #1e40af;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .job-info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .job-info-item {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        border: 1px solid #e2e8f0;
    }
    
    .job-info-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    .job-info-value {
        font-size: 1rem;
        color: #1e293b;
        font-weight: 600;
    }
    
    /* 成功ボックス */
    .success-box {
        background: #f0fdf4;
        border: 2px solid #22c55e;
        color: #15803d;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(34, 197, 94, 0.1);
    }
    
    .success-box h4 {
        color: #15803d;
        margin-bottom: 0.5rem;
    }
    
    /* 警告ボックス */
    .warning-box {
        background: #fffbeb;
        border: 2px solid #f59e0b;
        color: #d97706;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(245, 158, 11, 0.1);
    }
    
    .warning-box h4 {
        color: #d97706;
        margin-bottom: 0.5rem;
    }
    
    /* 情報ボックス */
    .info-box {
        background: #eff6ff;
        border: 2px solid #3b82f6;
        color: #1d4ed8;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
    }
    
    .info-box h4 {
        color: #1d4ed8;
        margin-bottom: 0.5rem;
    }
    
    /* メトリクスカード */
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
        border-color: #3b82f6;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e40af;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.3rem;
    }
    
    /* サイドバーセクション */
    .sidebar-section {
        background: #ffffff;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .sidebar-section h4 {
        color: #1e40af;
        margin-bottom: 0.8rem;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .sidebar-section p, .sidebar-section li {
        color: #475569;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    .sidebar-section ol li {
        margin-bottom: 0.5rem;
    }
    
    /* ステータスバッジ */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-created {
        background-color: #dcfce7;
        color: #15803d;
        border: 1px solid #22c55e;
    }
    
    .status-processing {
        background-color: #fef3c7;
        color: #d97706;
        border: 1px solid #f59e0b;
    }
    
    .status-completed {
        background-color: #dbeafe;
        color: #1d4ed8;
        border: 1px solid #3b82f6;
    }
    
    /* 小さなアイコン */
    .small-icon {
        font-size: 0.8rem;
        margin-right: 0.2rem;
    }
    
    /* セクションヘッダー */
    .section-header {
        color: #1e40af;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Streamlitコンポーネントのスタイル調整 */
    .stSelectbox > div > div {
        border: 2px solid #e2e8f0;
        border-radius: 8px;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    .stTextInput > div > div > input {
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        border: none;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e3a8a 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* ファイルアップローダー */
    .stFileUploader > div {
        border: 2px dashed #3b82f6;
        border-radius: 12px;
        background: #f8fafc;
        padding: 2rem;
        text-align: center;
    }
    
    .stFileUploader > div:hover {
        background: #eff6ff;
        border-color: #1d4ed8;
    }
    
    /* データフレーム */
    .stDataFrame {
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* エキスパンダー */
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        color: #1e40af;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #eff6ff;
        border-color: #3b82f6;
    }
    
    /* ダウンロードボタンの強調 */
    .download-section {
        background: #f0fdf4;
        border: 2px solid #22c55e;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* ダウンロードボタンのカスタムスタイル */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 1rem 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(34, 197, 94, 0.2) !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(34, 197, 94, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# ファイルベースのジョブ履歴管理
class JobHistoryManager:
    def __init__(self):
        self.history_file = Path("job_history.json")
        self.download_cache_dir = Path("download_cache")
        self.download_cache_dir.mkdir(exist_ok=True)
    
    def save_jobs(self, jobs):
        """ジョブ履歴をファイルに保存"""
        try:
            # datetime オブジェクトを文字列に変換
            serializable_jobs = []
            for job in jobs:
                job_copy = job.copy()
                if isinstance(job_copy.get('created_at'), datetime):
                    job_copy['created_at'] = job_copy['created_at'].isoformat()
                serializable_jobs.append(job_copy)
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_jobs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            st.error(f"ジョブ履歴の保存に失敗しました: {str(e)}")
    
    def load_jobs(self):
        """ジョブ履歴をファイルから読み込み"""
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                jobs = json.load(f)
            
            # 文字列をdatetimeオブジェクトに変換
            for job in jobs:
                if isinstance(job.get('created_at'), str):
                    job['created_at'] = datetime.fromisoformat(job['created_at'])
            
            # 作成日時の降順でソート
            jobs.sort(key=lambda x: x['created_at'], reverse=True)
            return jobs
        except Exception as e:
            st.error(f"ジョブ履歴の読み込みに失敗しました: {str(e)}")
            return []
    
    def add_job(self, job):
        """新しいジョブを追加"""
        jobs = self.load_jobs()
        jobs.insert(0, job)
        self.save_jobs(jobs)
    
    def update_job(self, job_id, updates):
        """ジョブを更新"""
        jobs = self.load_jobs()
        for job in jobs:
            if job['job_id'] == job_id:
                job.update(updates)
                break
        self.save_jobs(jobs)
    
    def get_job(self, job_id):
        """特定のジョブを取得"""
        jobs = self.load_jobs()
        for job in jobs:
            if job['job_id'] == job_id:
                return job
        return None
    
    def cache_download_file(self, job_id, file_type, df):
        """ダウンロード用ファイルをキャッシュ"""
        cache_path = self.download_cache_dir / f"{job_id}_{file_type}.xlsx"
        df.to_excel(cache_path, index=False)
        return cache_path

# データ処理マネージャー
class DataManager:
    def __init__(self):
        self.base_dir = Path("jobs")
        self.base_dir.mkdir(exist_ok=True)
    
    def normalize_text(self, text):
        """テキストを正規化（全角→半角、空白削除など）"""
        if pd.isna(text):
            return ""
        text = str(text)
        # 全角英数字を半角に変換
        text = text.translate(str.maketrans(
            'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９',
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        ))
        # 空白を削除
        text = re.sub(r'\s+', '', text)
        return str(text).strip()
    
    def normalize_phone(self, phone_str):
        """電話番号を正規化（+81形式を0始まりに変換）"""
        if pd.isna(phone_str):
            return ""
        phone_str = str(phone_str).strip()
        # +81を0に変換
        phone_str = re.sub(r'^\+81\s*', '0', phone_str)
        # ハイフンやスペースを削除
        phone_str = re.sub(r'[\s\-()]', '', phone_str)
        return str(phone_str).strip()
    
    def create_row_key(self, company, phone=""):
        """行指紋を作成（社名ベース、電話番号はオプション）"""
        # 社名を正規化してキーとして使用
        normalized_company = self.normalize_text(company)
        normalized_phone = self.normalize_phone(phone) if phone else ""
        base = f"{normalized_company}|{normalized_phone}"
        return hashlib.sha256(base.encode('utf-8')).hexdigest()[:16]
    
    def process_filemaker_data(self, df, job_id, output_filename):
        """税理士アポシスCSVデータを処理"""
        job_dir = self.base_dir / job_id
        job_dir.mkdir(exist_ok=True)
        
        # 元データを保存
        original_path = job_dir / "fm_export.csv"
        df.to_csv(original_path, index=False, encoding='utf-8-sig')
        
        # AIテレアポ用にデータを変換
        upload_df = df.copy()
        
        # 税理士アポシスCSVの場合、「社名」列と「住所統合」列がある
        # 電話番号列がない場合は空列を追加
        if '電話番号' not in upload_df.columns:
            upload_df['電話番号'] = ""
        
        # 必要な列のみ抽出（AIテレアポ用）
        required_columns = ['社名', '電話番号', '住所統合']
        available_columns = [col for col in required_columns if col in upload_df.columns]
        
        if available_columns:
            upload_df = upload_df[available_columns].copy()
        
        # 社名を50文字でカット
        if '社名' in upload_df.columns:
            upload_df['社名'] = upload_df['社名'].astype(str).str[:50]
        
        # 行指紋を作成してrowmapを生成(社名ベース)
        rowmap_data = []
        for idx, row in df.iterrows():
            company = row.get('社名', '')
            phone = row.get('電話番号', '') if '電話番号' in df.columns else ''
            row_key = self.create_row_key(company, phone)
            
            rowmap_data.append({
                'row_key': row_key,
                'company': company,
                'company_normalized': self.normalize_text(company),
                'phone': phone,
                'address': row.get('住所統合', ''),
                'index_in_fm': idx
            })
        
        rowmap_df = pd.DataFrame(rowmap_data)
        rowmap_path = job_dir / "rowmap.csv"
        rowmap_df.to_csv(rowmap_path, index=False, encoding='utf-8-sig')
        
        # アップロード用CSVを保存（UTF-8 with BOM）
        upload_path = job_dir / f"{output_filename}.csv"
        try:
            # まずShift-JISを試す
            upload_df.to_csv(upload_path, index=False, encoding='shift_jis')
        except UnicodeEncodeError:
            # Shift-JISで保存できない場合はUTF-8 with BOMを使用
            upload_df.to_csv(upload_path, index=False, encoding='utf-8-sig')
        
        # マニフェストを作成
        manifest = {
            'job_id': job_id,
            'created_at': datetime.now().isoformat(),
            'original_filename': output_filename,
            'total_rows': len(df),
            'files': {
                'fm_export': 'fm_export.csv',
                'upload': f'{output_filename}.csv',
                'rowmap': 'rowmap.csv'
            }
        }
        
        manifest_path = job_dir / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        return {
            'job_id': job_id,
            'upload_path': upload_path,
            'total_rows': len(df),
            'manifest': manifest
        }
    
    def analyze_call_results(self, df):
        """通話結果を分析"""
        # 電話番号を正規化
        if '電話番号' in df.columns:
            df["電話番号"] = df["電話番号"].astype(str).str.replace(r'^\+81\s*', '0', regex=True)
            df["電話番号"] = df["電話番号"].str.replace(" ", "")
        
        # 通話時間を数値化
        df["通話時間_num"] = pd.to_numeric(df["通話時間"], errors="coerce")
        
        # 断り・終了系ワード
        ng_words = [
            "断り", "不要", "必要ない", "結構です", "結構",
            "電話が終了", "電話を切った", "切断", "応答なし", "応答無し",
            "切られ", "切られる", "切った", "通話が終了", "会話が終了",
            "進展しない", "通話を終了", "進まなかった", "切りました", "断念",
            "終了", "成立しなかった", "切", "進展はありま"
        ]
        
        # ステータス分類
        for idx, row in df.iterrows():
            status = str(row["ステータス"])
            result = str(row["架電結果"]) if pd.notna(row["架電結果"]) else ""
            summary = str(row["要約"]) if pd.notna(row["要約"]) else ""
            duration = row["通話時間_num"]
            
            # 既に結果が入っている場合はスキップ
            if result.strip() != "" and result.strip() != "nan":
                continue
            
            # 留守番電話 → 留守電
            if status.strip() == "留守番電話":
                df.at[idx, "架電結果"] = "留守電"
                continue
            
            # 応答なし → 留守
            if status.strip() in ["応答なし", "応答無し"]:
                df.at[idx, "架電結果"] = "留守"
                continue
            
            # 獲得 → AI電話APO
            if status.strip() == "獲得":
                df.at[idx, "架電結果"] = "AI電話APO"
                continue
            
            # 要約に断りワードが含まれる → NG
            if any(word in summary for word in ng_words):
                df.at[idx, "架電結果"] = "NG"
                continue
            
            # 通話時間が0 → 留守
            if duration == 0:
                df.at[idx, "架電結果"] = "留守"
                continue
            
            # ステータスが自動音声 → 留守電
            if status.strip() == "自動音声":
                df.at[idx, "架電結果"] = "留守電"
                continue
            
            # 要約に「応答なし」 → 留守
            if any(x in summary for x in ["応答なし", "応答無し"]):
                df.at[idx, "架電結果"] = "留守"
                continue
            
            # 要約に「転送」や「了承しました」など → 電話APO
            if any(x in summary for x in ["転送された", "了承しました", "転送されました"]):
                df.at[idx, "架電結果"] = "AI電話APO"
                continue
            
            # 通話時間あり & 転送でない → NG
            if pd.notna(duration) and duration > 0 and not any(x in summary for x in ["転送"]):
                df.at[idx, "架電結果"] = "NG"
        
        return df
    
    def merge_with_original(self, call_results_df, job_id):
        """元データとマージ（社名ベース）"""
        job_dir = self.base_dir / job_id
        
        # マニフェストを読み込み
        manifest_path = job_dir / "manifest.json"
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # rowmapを読み込み
        rowmap_path = job_dir / "rowmap.csv"
        rowmap_df = pd.read_csv(rowmap_path, encoding='utf-8-sig')
        
        # 元データを読み込み
        original_path = job_dir / "fm_export.csv"
        original_df = pd.read_csv(original_path, encoding='utf-8-sig')
        
        # 通話結果の社名を正規化
        call_results_df['社名_正規化'] = call_results_df['社名'].apply(self.normalize_text)
        
        # 架電時刻列を保持（存在する場合）
        has_call_time = '架電時刻' in call_results_df.columns
        
        # 架電時刻を日付と時間に分割
        if has_call_time:
            try:
                # 架電時刻を日時型に変換
                call_results_df['架電時刻_dt'] = pd.to_datetime(call_results_df['架電時刻'], errors='coerce')
                # 日付列を作成（YYYY/MM/DD形式）
                call_results_df['架電日'] = call_results_df['架電時刻_dt'].dt.strftime('%Y/%m/%d')
                # 時間列を作成（HH:MM:SS形式）
                call_results_df['架電時間'] = call_results_df['架電時刻_dt'].dt.strftime('%H:%M:%S')
                # 一時列を削除
                call_results_df = call_results_df.drop('架電時刻_dt', axis=1)
            except Exception as e:
                # エラーが発生した場合は元の架電時刻をそのまま使用
                pass
        
        # 社名ベースでマージ
        merged_df = pd.merge(
            call_results_df, 
            rowmap_df[['company_normalized', 'company', 'address']], 
            left_on='社名_正規化', 
            right_on='company_normalized', 
            how='left'
        )
        
        # 通話結果に行指紋を追加
        merged_df['row_key'] = merged_df.apply(
            lambda row: self.create_row_key(row.get('社名', ''), row.get('電話番号', '')), 
            axis=1
        )
        
        # 列の順序を整理（架電日・架電時間を含める）
        if has_call_time and '架電日' in merged_df.columns and '架電時間' in merged_df.columns:
            column_order = ['社名', '電話番号', '架電日', '架電時間', 'ステータス', '架電結果', '要約', '通話時間', 
                           '住所統合', 'row_key']
        elif has_call_time:
            # 分割できなかった場合は元の架電時刻を使用
            column_order = ['社名', '電話番号', '架電時刻', 'ステータス', '架電結果', '要約', '通話時間', 
                           '住所統合', 'row_key']
        else:
            column_order = ['社名', '電話番号', 'ステータス', '架電結果', '要約', '通話時間', 
                           '住所統合', 'row_key']
        
        # 住所統合列を元データから取得
        if 'address' in merged_df.columns:
            merged_df['住所統合'] = merged_df['address']
        
        # 存在する列のみを選択
        available_columns = [col for col in column_order if col in merged_df.columns]
        merged_df = merged_df[available_columns]
        
        return merged_df
    
    def calculate_statistics(self, df):
        """統計を計算"""
        def parse_duration(val):
            if pd.isna(val):
                return 0
            val = str(val).strip()
            if val in ["", "-", "nan"]:
                return 0
            parts = val.split(":")
            try:
                if len(parts) == 3:  # hh:mm:ss
                    h, m, s = map(int, parts)
                    return h*3600 + m*60 + s
                elif len(parts) == 2:  # mm:ss
                    m, s = map(int, parts)
                    return m*60 + s
                else:
                    return int(val)  # 秒数
            except:
                return 0
        
        # 通話時間を秒に変換
        df["通話時間_sec"] = df["通話時間"].apply(parse_duration)
        
        # 統計計算
        total_calls = len(df)
        result_counts = df["架電結果"].value_counts()
        valid_calls = df[~df["架電結果"].isin(["留守", "留守番電話"])].shape[0]
        total_time_sec = int(df["通話時間_sec"].sum())
        total_time_str = str(timedelta(seconds=total_time_sec))
        transfer_calls = df[df["架電結果"].str.contains("APO", na=False)].shape[0]
        
        # 無効番号（電話番号列がある場合のみ）
        invalid_numbers = 0
        if '電話番号' in df.columns:
            df["電話番号_str"] = df["電話番号"].astype(str).str.replace(r"\D", "", regex=True)
            invalid_numbers = df[~df["電話番号_str"].str.match(r"^0\d{9,10}$", na=False)].shape[0]
        
        # エラー件数
        error_calls = df[df[["ステータス", "要約"]].astype(str).apply(
            lambda x: any("エラー" in v for v in x), axis=1
        )].shape[0]
        
        return {
            'total_calls': total_calls,
            'valid_calls': valid_calls,
            'total_time': total_time_str,
            'transfer_calls': transfer_calls,
            'invalid_numbers': invalid_numbers,
            'error_calls': error_calls,
            'result_counts': result_counts.to_dict()
        }

# 改良されたジョブカード表示関数
def display_job_card(job):
    """見やすいジョブカードを表示"""
    status_class = f"status-{job.get('status', 'created')}"
    created_at = job['created_at']
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
    
    status_emoji = {
        'created': '✅',
        'processing': '⏳',
        'completed': '🎉'
    }
    
    status_text = {
        'created': '作成済み',
        'processing': '処理中',
        'completed': '完了'
    }
    
    st.markdown(f"""
    <div class="job-card">
        <div class="job-card-header">
            <span>{status_emoji.get(job.get('status', 'created'), '📄')} {job['filename']}</span>
            <span class="status-badge {status_class}">{status_text.get(job.get('status', 'created'), '不明')}</span>
        </div>
        <div class="job-info-grid">
            <div class="job-info-item">
                <div class="job-info-label">📅 作成日時</div>
                <div class="job-info-value">{created_at.strftime('%Y/%m/%d %H:%M')}</div>
            </div>
            <div class="job-info-item">
                <div class="job-info-label">🔢 ジョブID</div>
                <div class="job-info-value">{job['job_id'][:8]}...</div>
            </div>
            <div class="job-info-item">
                <div class="job-info-label">📊 件数</div>
                <div class="job-info-value">{job['total_rows']:,}件</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# メイン処理
def main():
    st.markdown('<h1 class="main-header">📞 AIテレアポ管理システム（税理士アポシス版）</h1>', unsafe_allow_html=True)
    
    # マネージャーの初期化
    history_manager = JobHistoryManager()
    data_manager = DataManager()
    
    # サイドバー
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-section">
            <h4>📖 使い方</h4>
            <ol>
                <li><strong>CSVファイルをアップロード</strong><br>税理士アポシスのCSVファイル（社名、住所統合列を含む）</li>
                <li><strong>AIテレアポ用CSVを生成</strong><br>ダウンロードしてAIテレアポシステムにアップロード</li>
                <li><strong>通話結果をアップロード</strong><br>AIテレアポから返却されたCSVをアップロード</li>
                <li><strong>分析結果をダウンロード</strong><br>元データとマージされた結果を取得</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-section">
            <h4>ℹ️ 注意事項</h4>
            <p>• 税理士アポシスCSVは「社名」「住所統合」列が必須です</p>
            <p>• 電話番号列がない場合は空列が追加されます</p>
            <p>• 社名は50文字まで自動カットされます</p>
            <p>• 通話結果は社名ベースでマッチングされます</p>
        </div>
        """, unsafe_allow_html=True)
    
    # タブの作成
    tab1, tab2 = st.tabs(["📤 新規アップロード", "📋 ジョブ履歴"])
    
    with tab1:
        st.markdown('<h2 class="section-header">📤 税理士アポシスCSVのアップロード</h2>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "税理士アポシスのCSVファイルを選択してください",
            type=['csv'],
            help="社名、住所統合列を含むCSVファイルをアップロードしてください"
        )
        
        if uploaded_file:
            try:
                # CSVを読み込み（UTF-8 with BOMに対応）
                df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
                
                st.markdown(f"""
                <div class="info-box">
                    <h4>✅ ファイル読み込み成功</h4>
                    <p><strong>ファイル名:</strong> {uploaded_file.name}</p>
                    <p><strong>データ件数:</strong> {len(df):,}件</p>
                    <p><strong>列数:</strong> {len(df.columns)}列</p>
                </div>
                """, unsafe_allow_html=True)
                
                # データプレビュー
                with st.expander("📊 データプレビュー", expanded=True):
                    st.dataframe(df.head(10), use_container_width=True)
                
                # 列の確認
                required_cols = ['社名', '住所統合']
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    st.markdown(f"""
                    <div class="warning-box">
                        <h4>⚠️ 必須列が不足しています</h4>
                        <p>以下の列が見つかりません: {', '.join(missing_cols)}</p>
                        <p>税理士アポシスCSVには「社名」「住所統合」列が必要です。</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # 処理実行ボタン
                    if st.button("🚀 AIテレアポ用CSVを生成", type="primary", use_container_width=True):
                        with st.spinner("処理中..."):
                            # ジョブIDを生成
                            job_id = hashlib.sha256(f"{uploaded_file.name}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
                            
                            # 出力ファイル名
                            output_filename = uploaded_file.name.replace('.csv', '_ai_teleapo')
                            
                            # データ処理
                            result = data_manager.process_filemaker_data(df, job_id, output_filename)
                            
                            # ジョブを履歴に追加
                            job = {
                                'job_id': job_id,
                                'filename': uploaded_file.name,
                                'created_at': datetime.now(),
                                'total_rows': result['total_rows'],
                                'status': 'created'
                            }
                            history_manager.add_job(job)
                            
                            st.markdown(f"""
                            <div class="success-box">
                                <h4>🎉 処理完了!</h4>
                                <p><strong>ジョブID:</strong> {job_id}</p>
                                <p><strong>処理件数:</strong> {result['total_rows']:,}件</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # ダウンロードボタン
                            with open(result['upload_path'], 'rb') as f:
                                st.download_button(
                                    label="📥 AIテレアポ用CSVをダウンロード",
                                    data=f.read(),
                                    file_name=f"{output_filename}.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            
                            st.info("💡 このCSVをAIテレアポシステムにアップロードしてください。通話完了後、結果CSVを「ジョブ履歴」タブからアップロードできます。")
            
            except Exception as e:
                st.markdown(f"""
                <div class="warning-box">
                    <h4>❌ エラーが発生しました</h4>
                    <p>{str(e)}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 class="section-header">📋 ジョブ履歴</h2>', unsafe_allow_html=True)
        
        jobs = history_manager.load_jobs()
        
        if not jobs:
            st.markdown("""
            <div class="info-box">
                <h4>📭 ジョブ履歴がありません</h4>
                <p>「新規アップロード」タブからCSVファイルをアップロードしてください。</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # ジョブ選択
            job_options = {f"{job['filename']} ({job['created_at'].strftime('%Y/%m/%d %H:%M')})": job['job_id'] for job in jobs}
            selected_job_name = st.selectbox("📂 ジョブを選択", list(job_options.keys()))
            selected_job_id = job_options[selected_job_name]
            
            # 選択されたジョブの詳細表示
            selected_job = history_manager.get_job(selected_job_id)
            if selected_job:
                display_job_card(selected_job)
                
                # 通話結果のアップロード
                st.markdown('<h3 class="section-header">📥 通話結果のアップロード</h3>', unsafe_allow_html=True)
                
                call_result_file = st.file_uploader(
                    "AIテレアポからの通話結果CSVをアップロード",
                    type=['csv'],
                    key=f"call_result_{selected_job_id}"
                )
                
                if call_result_file:
                    try:
                        # 通話結果を読み込み
                        call_results_df = pd.read_csv(call_result_file, encoding='utf-8-sig')
                        
                        st.markdown(f"""
                        <div class="info-box">
                            <h4>✅ 通話結果読み込み成功</h4>
                            <p><strong>通話件数:</strong> {len(call_results_df):,}件</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # データプレビュー
                        with st.expander("📊 通話結果プレビュー"):
                            st.dataframe(call_results_df.head(10), use_container_width=True)
                        
                        # 分析実行ボタン
                        if st.button("🔍 分析を実行", type="primary", use_container_width=True):
                            with st.spinner("分析中..."):
                                # 通話結果を分析
                                analyzed_df = data_manager.analyze_call_results(call_results_df)
                                
                                # 統計を計算
                                stats = data_manager.calculate_statistics(analyzed_df)
                                
                                # 統計表示
                                st.markdown('<h3 class="section-header">📊 分析結果</h3>', unsafe_allow_html=True)
                                
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    st.markdown(f"""
                                    <div class="metric-card">
                                        <div class="metric-value">{stats['total_calls']}</div>
                                        <div class="metric-label">📞 総架電数</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with col2:
                                    st.markdown(f"""
                                    <div class="metric-card">
                                        <div class="metric-value">{stats['valid_calls']}</div>
                                        <div class="metric-label">✅ 有効架電数</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with col3:
                                    st.markdown(f"""
                                    <div class="metric-card">
                                        <div class="metric-value">{stats['transfer_calls']}</div>
                                        <div class="metric-label">🎯 APO獲得数</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                with col4:
                                    apo_rate = (stats['transfer_calls'] / stats['valid_calls'] * 100) if stats['valid_calls'] > 0 else 0
                                    st.markdown(f"""
                                    <div class="metric-card">
                                        <div class="metric-value">{apo_rate:.1f}%</div>
                                        <div class="metric-label">📈 APO率</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                # 架電結果の内訳
                                st.markdown('<h4>📋 架電結果の内訳</h4>', unsafe_allow_html=True)
                                result_df = pd.DataFrame(list(stats['result_counts'].items()), columns=['架電結果', '件数'])
                                result_df['割合'] = (result_df['件数'] / stats['total_calls'] * 100).round(1).astype(str) + '%'
                                st.dataframe(result_df, use_container_width=True)
                                
                                # 元データとマージ（社名ベース）
                                merged_df = data_manager.merge_with_original(analyzed_df, selected_job_id)
                                
                                st.markdown('<h4>📄 マージ済みデータ</h4>', unsafe_allow_html=True)
                                st.dataframe(merged_df, use_container_width=True)
                                
                                # ダウンロードボタン
                                st.markdown('<div class="download-section">', unsafe_allow_html=True)
                                st.markdown('<h4>💾 結果をダウンロード</h4>', unsafe_allow_html=True)
                                
                                # Excelファイルとして保存
                                output = BytesIO()
                                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                    merged_df.to_excel(writer, sheet_name='通話結果', index=False)
                                output.seek(0)
                                
                                st.download_button(
                                    label="📥 分析結果をダウンロード (Excel)",
                                    data=output,
                                    file_name=f"{selected_job['filename'].replace('.csv', '')}_分析結果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True
                                )
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                # ジョブステータスを更新
                                history_manager.update_job(selected_job_id, {'status': 'completed'})
                                
                    except Exception as e:
                        st.markdown(f"""
                        <div class="warning-box">
                            <h4>❌ エラーが発生しました</h4>
                            <p>{str(e)}</p>
                        </div>
                        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
