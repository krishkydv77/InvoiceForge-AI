# InvoiceForge AI

### Intelligent Invoice Processing, Data Masking & Automation Platform

> **Extract intelligently. Validate accurately. Mask securely. Generate professionally.**

InvoiceForge AI is an AI-powered invoice intelligence and automation platform designed to automate the invoice processing lifecycle — from multi-format document ingestion and AI-powered data extraction to validation, secure database storage, sensitive-data masking, and professional PDF generation.

The platform combines **Generative AI, document processing, data validation, MySQL persistence, sensitive-data masking, and automated PDF generation** into a modular FastAPI-based architecture.



##  Overview

Traditional invoice processing often involves manually reading documents, extracting customer and item information, validating invoice data, entering records into databases, and generating or sharing invoices.

**InvoiceForge AI** automates this workflow using AI and backend automation.

```text
Invoice Document
       │
       ▼
Document Processing
       │
       ▼
AI-Powered Extraction
       │
       ▼
Structured Invoice Data
       │
       ▼
Data Validation
       │
       ▼
MySQL Persistence
       │
       ▼
Sensitive Data Masking
       │
       ▼
Professional PDF Generation
```



##  Key Features

-  AI-powered invoice data extraction using Google Gemini
-  Multi-format invoice/document processing
-  Automated invoice data validation
-  Sensitive customer data masking
-  MySQL database persistence
-  Professional PDF invoice generation
-  FastAPI REST API
-  Swagger / OpenAPI documentation
-  Modular backend architecture
-  Environment-based secret management
-  Structured error handling
-  Structured invoice data processing



#  High-Level Architecture

```text
                         ┌──────────────────────────┐
                         │          USER            │
                         │                          │
                         │ Invoice / Document Input │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │       FastAPI API        │
                         │                          │
                         │ REST Endpoints           │
                         │ Request Validation       │
                         │ Error Handling            │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │    Invoice Service       │
                         │                          │
                         │ Business Logic           │
                         │ Workflow Orchestration   │
                         └────────────┬─────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
              ▼                       ▼                       ▼
     ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
     │ Document       │     │   Gemini AI    │     │  Validation    │
     │ Processing     │     │                │     │    Engine       │
     │                │     │ Invoice        │     │                │
     │ PDF            │     │ Extraction     │     │ Field Checks   │
     │ Images         │     │                │     │ Item Checks    │
     │ DOCX           │     │ Structured     │     │ Data Checks    │
     │ XLSX / CSV     │     │ Output         │     │                │
     └───────┬────────┘     └───────┬────────┘     └───────┬────────┘
             │                      │                      │
             └──────────────────────┼──────────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────────┐
                         │   Structured Invoice     │
                         │          Data            │
                         └────────────┬─────────────┘
                                      │
                         ┌────────────┴─────────────┐
                         │                          │
                         ▼                          ▼
                ┌──────────────────┐      ┌────────────────────┐
                │      MySQL       │      │  PDF Generation    │
                │     Database     │      │                    │
                │                  │      │ Data Masking       │
                │ Invoice Storage  │      │ Document Formatting│
                └──────────────────┘      └─────────┬──────────┘
                                                    │
                                                    ▼
                                      ┌────────────────────────┐
                                      │   Secure Generated     │
                                      │      Invoice PDF       │
                                      └────────────────────────┘
```



# Invoice Processing Workflow

```text
                 Invoice Upload
                       │
                       ▼
                Detect File Type
                       │
                       ▼
                 Parse Document
                       │
                       ▼
             Extract Invoice Content
                       │
                       ▼
                Gemini AI Processing
                       │
                       ▼
              Structured Invoice Data
                       │
                       ▼
                  Data Validation
                       │
                ┌──────┴──────┐
                │             │
             Invalid         Valid
                │             │
                ▼             ▼
          Return Error    Store in MySQL
                              │
                              ▼
                      Apply Data Masking
                              │
                              ▼
                       Generate PDF
                              │
                              ▼
                     Final Invoice Output
```



#  Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| AI / LLM | Google Gemini |
| GenAI SDK | Google GenAI |
| Database | MySQL |
| ORM | SQLAlchemy |
| Database Driver | PyMySQL |
| API Server | Uvicorn |
| Data Validation | Pydantic |
| PDF Generation | ReportLab |
| Document Processing | PDF / Image / DOCX / Excel / CSV |
| API Documentation | Swagger / OpenAPI |
| Configuration | python-dotenv |
| Version Control | Git / GitHub |
| Package Management | uv / pip |




#  Installation & Setup

## Prerequisites

- Python 3.11+
- MySQL
- Git
- Google Gemini API Key

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/InvoiceForge-AI.git
cd InvoiceForge-AI
```

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scriptsctivate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or:

```bash
uv pip install -r requirements.txt
```

### Swagger UI

```text
http://127.0.0.1:8000/docs
```



#  Project Objective

The objective of InvoiceForge AI is to reduce manual invoice-processing effort by combining **Generative AI, document processing, structured validation, database automation, sensitive-data protection, and automated document generation** into a unified platform.

```text
Unstructured Invoice
        │
        ▼
   AI Extraction
        │
        ▼
 Structured Data
        │
        ▼
    Validation
        │
        ▼
 Secure Persistence
        │
        ▼
 Sensitive Data Masking
        │
        ▼
 Professional PDF
```

---

#  Skills Demonstrated

```text
Python
FastAPI
Generative AI
Google Gemini
LLM Integration
REST API Development
Document Intelligence
Data Validation
MySQL
SQLAlchemy
PyMySQL
PDF Generation
Data Masking
Streamlit
Backend Architecture
API Design
Environment Configuration
Git & GitHub
```



<div align="center">

## InvoiceForge AI

### Intelligent Invoice Processing, Data Masking & Automation Platform

**Extract intelligently. Validate accurately. Mask securely. Generate professionally.**

</div>
