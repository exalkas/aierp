# File Storage & Document Management Specification

## Document Information

- **Version**: 1.0
- **Date**: January 2025
- **Purpose**: Complete file storage system specification
- **Scope**: All file management across CRM, ERP, and admin modules

---

## 1. OVERVIEW

### 1.1 System Requirements

**Core File Management Needs:**

- Customer documents (contracts, IDs, invoices)
- Product images and specifications
- Employee documents (contracts, certificates)
- Company documents (licenses, certifications)
- Financial documents (receipts, bank statements)
- Communication attachments (emails, messages)
- System backups and exports

**Greek-Specific Requirements:**

- Greek filename support (UTF-8 encoding)
- AADE-compliant document storage
- Greek legal document templates
- Multi-language file descriptions
- Greek tax document categorization

### 1.2 Technical Architecture

**Dual Deployment Storage Strategy:**

**SAAS Deployment (Cloud Storage):**

- **Primary Storage**: AWS S3 / Azure Blob Storage / Google Cloud Storage
- **File Identification**: UUID-based file IDs with cloud path mapping
- **CDN Integration**: CloudFront/Azure CDN for fast global access
- **Automatic Scaling**: Unlimited storage with usage-based billing
- **Built-in Redundancy**: Multi-region replication for disaster recovery
- **Security**: Server-side encryption, access controls, audit logging

**Local Installation (Filesystem Storage):**

- **Primary Storage**: Local filesystem with organized directory structure
- **File Identification**: Relative path-based with database mapping
- **Backup Integration**: Automated local backup with external storage options
- **Storage Limits**: Configurable quotas based on available disk space
- **Security**: File-level encryption, folder permissions, access controls
- **Migration Ready**: Structured format for easy SAAS migration

**Unified File Management API:**

- **Storage-Agnostic Interface**: Same API for both deployments
- **Automatic Backend Selection**: Based on deployment configuration
- **Migration Support**: Tools to move files between deployment types
- **Monitoring**: Unified monitoring regardless of storage backend

---

## 2. FILE STORAGE MODELS

### 2.1 Core File Model

```typescript
interface FileRecord {
  id: string; // UUID for SAAS, auto-increment for Local
  filename: string;
  originalFilename: string;
  mimetype: string;
  size: number;

  // Storage Details (Deployment-Specific)
  storageProvider: "local" | "aws_s3" | "azure_blob" | "gcp_storage";
  storagePath: string; // Full cloud path or relative local path
  storageUrl?: string; // CDN URL for SAAS, null for Local
  storageIdentifier: string; // UUID for SAAS, relative path for Local

  // Metadata
  title?: string;
  description?: string;
  tags: string[];
  category: string;

  // Security
  accessLevel: "public" | "private" | "restricted";
  encryptionKey?: string;

  // Relationships
  entityType: string; // 'customer', 'invoice', 'product', etc.
  entityId: string;
  folderId?: string;

  // Versioning
  version: number;
  previousVersionId?: string;
  isLatestVersion: boolean;

  // Greek-Specific
  greekCategory?: GreekDocumentCategory;
  aadeCompliant?: boolean;
  taxYear?: number;

  // Audit Trail
  uploadedBy: string;
  uploadedAt: Date;
  lastModifiedBy: string;
  lastModifiedAt: Date;

  // Processing Status
  processingStatus: "pending" | "processing" | "completed" | "failed";
  ocrText?: string;
  thumbnailPath?: string;
  previewPath?: string;

  // File Preview Capabilities
  previewSupported: boolean;
  previewType: FilePreviewType;
  previewUrl?: string;
  thumbnailUrl?: string;
  convertedFormats: ConvertedFormat[];
}

enum GreekDocumentCategory {
  TAX_DOCUMENTS = "tax_documents",
  LEGAL_DOCUMENTS = "legal_documents",
  CONTRACTS = "contracts",
  INVOICES = "invoices",
  RECEIPTS = "receipts",
  BANK_STATEMENTS = "bank_statements",
  GOVERNMENT_FORMS = "government_forms",
  LICENSES = "licenses",
  CERTIFICATES = "certificates",
  PERSONAL_DOCUMENTS = "personal_documents",
}

enum FilePreviewType {
  IMAGE = "image", // JPG, PNG, GIF, BMP, WEBP, SVG
  PDF = "pdf", // PDF documents
  VIDEO = "video", // MP4, AVI, MOV, WMV
  AUDIO = "audio", // MP3, WAV, AAC, OGG
  DOCUMENT = "document", // DOC, DOCX, RTF
  SPREADSHEET = "spreadsheet", // XLS, XLSX, CSV
  PRESENTATION = "presentation", // PPT, PPTX
  TEXT = "text", // TXT, MD, JSON, XML, HTML
  CODE = "code", // JS, TS, PY, PHP, CSS, etc.
  ARCHIVE = "archive", // ZIP, RAR, 7Z
  CAD = "cad", // DWG, DXF (for construction/engineering)
  NONE = "none", // No preview available
}

interface ConvertedFormat {
  format: string; // "pdf", "jpg", "html", "txt"
  url: string; // URL to converted file
  size: number; // Size of converted file
  createdAt: Date; // When conversion was done
  expiresAt?: Date; // When converted file expires (for temp conversions)
}

interface FilePreviewConfig {
  fileType: string; // MIME type or extension
  previewType: FilePreviewType;
  requiresConversion: boolean;
  conversionFormat?: string; // Target format for conversion
  maxFileSize: number; // Max file size for preview (in bytes)
  supportedFeatures: PreviewFeature[];
}

enum PreviewFeature {
  ZOOM = "zoom",
  PAGINATION = "pagination",
  SEARCH = "search",
  ANNOTATIONS = "annotations",
  DOWNLOAD = "download",
  PRINT = "print",
  FULLSCREEN = "fullscreen",
  ROTATE = "rotate",
  TEXT_SELECT = "text_select",
}
```

### 2.2 File Organization Model

```typescript
interface FileFolder {
  id: string;
  name: string;
  description?: string;
  parentId?: string;

  // Relationships
  entityType: string;
  entityId: string;

  // Permissions
  permissions: FolderPermission[];
  isPublic: boolean;

  // Greek-Specific
  greekLabel?: string;
  businessPurpose?: string;

  // Metadata
  createdBy: string;
  createdAt: Date;
  lastModifiedAt: Date;

  // Computed Properties
  fileCount?: number;
  totalSize?: number;
  subfolderCount?: number;
}

interface FolderPermission {
  userId: string;
  permission: "read" | "write" | "admin";
  grantedBy: string;
  grantedAt: Date;
}
```

---

## 3. FOLDER STRUCTURE & ORGANIZATION

### 3.1 Standardized Folder Structure

**SAAS Deployment Structure:**

```
/companies/{companyId}/
├── customers/
│   ├── {customerId}/
│   │   ├── contracts/
│   │   ├── correspondence/
│   │   ├── legal_documents/
│   │   ├── tax_documents/
│   │   └── general/
├── invoices/
│   ├── {year}/
│   │   ├── {month}/
│   │   │   ├── {invoiceId}/
│   │   │   │   ├── invoice.pdf
│   │   │   │   ├── receipt.pdf
│   │   │   │   └── supporting_docs/
├── products/
│   ├── {productId}/
│   │   ├── images/
│   │   ├── specifications/
│   │   └── documentation/
├── employees/
│   ├── {employeeId}/
│   │   ├── contracts/
│   │   ├── certificates/
│   │   ├── hr_documents/
│   │   └── performance_reviews/
├── company/
│   ├── legal/
│   ├── financial/
│   ├── licenses/
│   ├── policies/
│   └── templates/
└── backups/
    ├── {date}/
    └── exports/
```

**Local Installation Structure:**

```
./erp_data/
├── companies/
│   ├── {companyId}/
│   │   ├── customers/
│   │   │   ├── {customerId}/
│   │   │   │   ├── contracts/
│   │   │   │   ├── correspondence/
│   │   │   │   ├── legal_documents/
│   │   │   │   ├── tax_documents/
│   │   │   │   └── general/
│   │   ├── invoices/
│   │   │   ├── {year}/
│   │   │   │   ├── {month}/
│   │   │   │   │   ├── {invoiceId}/
│   │   │   │   │   │   ├── invoice.pdf
│   │   │   │   │   │   ├── receipt.pdf
│   │   │   │   │   │   └── supporting_docs/
│   │   ├── products/
│   │   ├── employees/
│   │   ├── company/
│   │   └── backups/
├── system/
│   ├── logs/
│   ├── temp/
│   └── config/
└── shared/
    ├── templates/
    └── resources/
```

### 3.2 File Identification Strategy

**SAAS File Identification:**

```typescript
interface SAASFileIdentifier {
  fileId: string; // UUID: "f47ac10b-58cc-4372-a567-0e02b2c3d479"
  bucketName: string; // "erp-files-production"
  objectKey: string; // "companies/123/customers/456/contracts/contract_2025.pdf"
  cdnUrl?: string; // "https://cdn.example.com/files/f47ac10b-58cc-4372-a567-0e02b2c3d479"

  // Metadata for quick access
  companyId: string;
  entityType: string; // "customer", "invoice", "product"
  entityId: string;
  category: string; // "contracts", "invoices", "images"
}
```

**Local File Identification:**

```typescript
interface LocalFileIdentifier {
  fileId: number; // Auto-increment: 1, 2, 3, etc.
  relativePath: string; // "companies/123/customers/456/contracts/contract_2025.pdf"
  absolutePath: string; // "/var/erp_data/companies/123/customers/456/contracts/contract_2025.pdf"

  // Metadata for organization
  companyId: string;
  entityType: string;
  entityId: string;
  category: string;

  // Local-specific
  fileSystemInfo: {
    permissions: string; // "644"
    owner: string;
    group: string;
    createdAt: Date;
    modifiedAt: Date;
  };
}
```

### 3.3 File Management Operations

**Core Operations (Both Deployments):**

```typescript
interface FileOperations {
  // Basic CRUD Operations
  uploadFile(file: File, metadata: FileMetadata): Promise<FileRecord>;
  viewFile(fileId: string): Promise<FileViewResponse>;
  deleteFile(fileId: string): Promise<boolean>;

  // Organization Operations
  createFolder(parentId: string, name: string): Promise<FileFolder>;
  moveFile(fileId: string, destinationFolderId: string): Promise<boolean>;
  copyFile(fileId: string, destinationFolderId: string): Promise<FileRecord>;

  // Batch Operations
  uploadMultipleFiles(
    files: File[],
    metadata: FileMetadata[]
  ): Promise<FileRecord[]>;
  deleteMultipleFiles(fileIds: string[]): Promise<boolean>;

  // Search & Filter
  searchFiles(query: string, filters: FileFilters): Promise<FileRecord[]>;
  listFiles(
    folderId: string,
    pagination: PaginationOptions
  ): Promise<FileListResponse>;

  // Sharing & Permissions
  shareFile(fileId: string, shareOptions: ShareOptions): Promise<FileShare>;
  setFilePermissions(
    fileId: string,
    permissions: FilePermission[]
  ): Promise<boolean>;
}
```

---

## 4. FILE MANAGEMENT INTERFACE

### 4.1 File Manager Layout

```
┌─ File Manager ────────────────────────────────────────────────┐
│ [📁 Back] Customer: ACME Corp                    [+ Upload] [⚙] │
│ ──────────────────────────────────────────────────────────────── │
│ Path: [🏠 Root] / [📁 Contracts] / [📁 2025]                    │
│ ──────────────────────────────────────────────────────────────── │
│ ┌─ Folder Tree ─────┐ ┌─ File List ─────────────────────────────┐ │
│ │ 📁 Contracts       │ │ ☐ [📄] Contract_2025.pdf    2.5MB    │ │
│ │   📁 2024          │ │ ☐ [📄] Addendum_v2.pdf      1.2MB    │ │
│ │   📁 2025 (active) │ │ ☐ [📊] Financial_Report.xlsx 3.8MB   │ │
│ │ 📁 Invoices        │ │ ☐ [🖼️] Company_Logo.png      0.5MB    │ │
│ │ 📁 Correspondence  │ │ ☐ [📹] Meeting_Recording.mp4 45MB    │ │
│ │ 📁 Legal Documents │ │                                       │ │
│ │ 📁 Marketing       │ │ Showing 5 of 23 files                │ │
│ │ [+ New Folder]     │ │ [🔍 Search] [Filter ▼] [Sort ▼] [⚙]   │ │
│ │                    │ │ [1] [2] [3] [4] [5] [Next →]         │ │
│ └────────────────────┘ └─────────────────────────────────────────┘ │
│ ──────────────────────────────────────────────────────────────── │
│ Selected: 2 files (4.7MB)  [📥 Download] [🔗 Share] [🗑️ Delete] │
└────────────────────────────────────────────────────────────────────┘
```

### 4.2 File Upload Interface

**Drag & Drop Upload Zone:**

```
┌─ Upload Files ────────────────────────────────────────────────┐
│ [× Close]                                          [Settings] │
│ ──────────────────────────────────────────────────────────────── │
│ ┌─ Drop Zone ─────────────────────────────────────────────────┐ │
│ │                                                             │ │
│ │    📁 Drag & Drop Files Here                              │ │
│ │         or [Browse Files]                                  │ │
│ │                                                             │ │
│ │  Supported: PDF, DOC, XLS, PNG, JPG, MP4, ZIP             │ │
│ │  Max size: 100MB per file                                  │ │
│ │                                                             │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ ──────────────────────────────────────────────────────────────── │
│ Upload Queue:                                                    │
│ ┌─ contract.pdf ─────────────────────────────── [████████] 100% │
│ │ Category: [Contracts ▼] Tags: [2025, annual]  [✓] Uploaded   │
│ └─────────────────────────────────────────────────────────────── │
│ ┌─ invoice_123.pdf ─────────────────────────── [████░░░░] 60%  │
│ │ Category: [Invoices ▼] Tags: [january, paid]  [⏸️] Pause     │
│ └─────────────────────────────────────────────────────────────── │
│ ──────────────────────────────────────────────────────────────── │
│ Upload Settings:                                                 │
│ ☑ Auto-categorize Greek documents                               │
│ ☑ Extract text (OCR) from images                               │
│ ☑ Generate thumbnails                                           │
│ ☐ Notify team members                                           │
│ ──────────────────────────────────────────────────────────────── │
│ [Cancel All]                                      [Upload All] │
└────────────────────────────────────────────────────────────────┘
```

### 4.3 File Preview Interface

**Advanced File Preview Modal:**

```
┌─ File Preview: Financial_Report.xlsx ─────────────────────────────┐
│ [← Back] [📥 Download] [🔗 Share] [🖨️ Print] [⛶ Fullscreen] [×] │
│ ─────────────────────────────────────────────────────────────────── │
│ ┌─ Preview Toolbar ────────────────────────────────────────────────┐ │
│ │ [🔍-] [100%] [🔍+] [↻] [↺] [🔍] [📄 1/3] [⚙️ Settings]        │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│ ┌─ Preview Area ──────────────────┐ ┌─ File Details ─────────────┐ │
│ │                                 │ │ Type: Excel Spreadsheet    │ │
│ │   [EXCEL SPREADSHEET PREVIEW]   │ │ Size: 3.8MB               │ │
│ │                                 │ │ Modified: Jan 16, 2025     │ │
│ │ Sheet: [Sales Data ▼]          │ │ By: Maria K.               │ │
│ │                                 │ │                            │ │
│ │ A    B      C      D     E      │ │ Preview Features:          │ │
│ │ 1  Month Sales  Profit Target   │ │ ✓ Interactive spreadsheet  │ │
│ │ 2  Jan   15K    3K     18K      │ │ ✓ Multiple sheets          │ │
│ │ 3  Feb   18K    4K     20K      │ │ ✓ Formula viewing          │ │
│ │ 4  Mar   22K    5K     25K      │ │ ✓ Chart previews           │ │
│ │                                 │ │                            │ │
│ │ [Show All Sheets] [Export View] │ │ Greek Category:            │ │
│ │                                 │ │ [Financial Reports ▼]     │ │
│ │                                 │ │                            │ │
│ │                                 │ │ AADE Compliant: ☑ Yes     │ │
│ │                                 │ │                            │ │
│ │                                 │ │ Versions:                  │ │
│ │                                 │ │ • v3.0 (current)          │ │
│ │                                 │ │ • v2.0 (Jan 15)           │ │
│ │                                 │ │ • v1.0 (Jan 10)           │ │
│ └─────────────────────────────────┘ └───────────────────────────┘ │
│ ─────────────────────────────────────────────────────────────────── │
│ ┌─ Preview Tabs ──────────────────────────────────────────────────┐ │
│ │ [📄 Document] [🖼️ Thumbnail] [📋 Properties] [💬 Comments]    │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

**File Type Specific Previews:**

**1. Image Preview:**

```
┌─ Image Preview: company_logo.png ─────────────────────────────────┐
│ [← Back] [📥 Download] [🔗 Share] [✏️ Edit] [🔄 Transform]   [×] │
│ ─────────────────────────────────────────────────────────────────── │
│ ┌─ Image Viewer ──────────────────────────────────────────────────┐ │
│ │ [🔍-] [Fit] [100%] [🔍+] [↻] [⛶] [🎨 Filters]               │ │
│ │                                                             │ │
│ │           [COMPANY LOGO IMAGE]                              │ │
│ │                                                             │ │
│ │ Original: 1920x1080 (2.1MP) • PNG • 0.5MB                  │ │
│ │ EXIF: Camera, Location, Date info available                │ │
│ └─────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

**2. PDF Preview:**

```
┌─ PDF Preview: contract_2025.pdf ──────────────────────────────────┐
│ [← Back] [📥 Download] [🔗 Share] [🖨️ Print] [📝 Annotate] [×] │
│ ─────────────────────────────────────────────────────────────────── │
│ ┌─ PDF Viewer ────────────────────────────────────────────────────┐ │
│ │ [🔍-] [75%] [🔍+] [📄 5/15] [🔍 Search] [💬 Comments]        │ │
│ │                                                             │ │
│ │           [PDF PAGE CONTENT]                                │ │
│ │                                                             │ │
│ │ Text is selectable and searchable                           │ │
│ │ Comments and annotations supported                          │ │
│ │ Bookmarks and outline available                             │ │
│ └─────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

**3. Word Document Preview:**

```
┌─ Document Preview: proposal.docx ─────────────────────────────────┐
│ [← Back] [📥 Download] [🔗 Share] [✏️ Edit Online] [📝 Comment] [×] │
│ ─────────────────────────────────────────────────────────────────── │
│ ┌─ Document Viewer ───────────────────────────────────────────────┐ │
│ │ [🔍-] [100%] [🔍+] [📄 2/8] [🔍 Find] [📋 Outline]           │ │
│ │                                                             │ │
│ │ Business Proposal                                           │ │
│ │ ================                                            │ │
│ │                                                             │ │
│ │ Executive Summary                                           │ │
│ │ This proposal outlines...                                   │ │
│ │                                                             │ │
│ │ [Document rendered with formatting preserved]               │ │
│ │ • Fonts, styles, and layout maintained                     │ │
│ │ • Tables and images displayed                               │ │
│ │ • Comments and track changes visible                       │ │
│ └─────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

**4. Video/Audio Preview:**

```
┌─ Media Preview: meeting_recording.mp4 ────────────────────────────┐
│ [← Back] [📥 Download] [🔗 Share] [✂️ Trim] [🎵 Extract Audio] [×] │
│ ─────────────────────────────────────────────────────────────────── │
│ ┌─ Media Player ──────────────────────────────────────────────────┐ │
│ │                                                             │ │
│ │           [VIDEO PLAYER]                                    │ │
│ │                                                             │ │
│ │ ▶️ [═══════════════════════════] 🔊 [═══] ⛶ ⚙️            │ │
│ │ 00:15:32 / 01:23:45 • 1080p • 45MB                        │ │
│ │                                                             │ │
│ │ Subtitles: [Auto-generated] [Upload SRT]                   │ │
│ │ Playback: [0.5x] [1x] [1.25x] [1.5x] [2x]                │ │
│ └─────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

### 4.4 File Preview Configuration

**Supported File Types for Preview:**

```typescript
const filePreviewSupport: FilePreviewConfig[] = [
  // Images
  {
    fileType: "image/jpeg",
    previewType: FilePreviewType.IMAGE,
    requiresConversion: false,
    maxFileSize: 50 * 1024 * 1024,
    supportedFeatures: [
      PreviewFeature.ZOOM,
      PreviewFeature.ROTATE,
      PreviewFeature.FULLSCREEN,
    ],
  },
  {
    fileType: "image/png",
    previewType: FilePreviewType.IMAGE,
    requiresConversion: false,
    maxFileSize: 50 * 1024 * 1024,
    supportedFeatures: [
      PreviewFeature.ZOOM,
      PreviewFeature.ROTATE,
      PreviewFeature.FULLSCREEN,
    ],
  },
  {
    fileType: "image/gif",
    previewType: FilePreviewType.IMAGE,
    requiresConversion: false,
    maxFileSize: 10 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.ZOOM, PreviewFeature.FULLSCREEN],
  },
  {
    fileType: "image/webp",
    previewType: FilePreviewType.IMAGE,
    requiresConversion: false,
    maxFileSize: 50 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.ZOOM, PreviewFeature.FULLSCREEN],
  },
  {
    fileType: "image/svg+xml",
    previewType: FilePreviewType.IMAGE,
    requiresConversion: false,
    maxFileSize: 5 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.ZOOM, PreviewFeature.FULLSCREEN],
  },

  // PDFs
  {
    fileType: "application/pdf",
    previewType: FilePreviewType.PDF,
    requiresConversion: false,
    maxFileSize: 100 * 1024 * 1024,
    supportedFeatures: [
      PreviewFeature.ZOOM,
      PreviewFeature.PAGINATION,
      PreviewFeature.SEARCH,
      PreviewFeature.TEXT_SELECT,
      PreviewFeature.ANNOTATIONS,
      PreviewFeature.PRINT,
    ],
  },

  // Microsoft Office Documents
  {
    fileType:
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    previewType: FilePreviewType.DOCUMENT,
    requiresConversion: true,
    conversionFormat: "html",
    maxFileSize: 25 * 1024 * 1024,
    supportedFeatures: [
      PreviewFeature.ZOOM,
      PreviewFeature.SEARCH,
      PreviewFeature.TEXT_SELECT,
    ],
  },
  {
    fileType: "application/msword",
    previewType: FilePreviewType.DOCUMENT,
    requiresConversion: true,
    conversionFormat: "html",
    maxFileSize: 25 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.ZOOM, PreviewFeature.SEARCH],
  },
  {
    fileType:
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    previewType: FilePreviewType.SPREADSHEET,
    requiresConversion: true,
    conversionFormat: "html",
    maxFileSize: 50 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.ZOOM, PreviewFeature.SEARCH],
  },
  {
    fileType: "application/vnd.ms-excel",
    previewType: FilePreviewType.SPREADSHEET,
    requiresConversion: true,
    conversionFormat: "html",
    maxFileSize: 50 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.ZOOM, PreviewFeature.SEARCH],
  },
  {
    fileType:
      "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    previewType: FilePreviewType.PRESENTATION,
    requiresConversion: true,
    conversionFormat: "html",
    maxFileSize: 50 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.ZOOM, PreviewFeature.PAGINATION],
  },

  // Text Files
  {
    fileType: "text/plain",
    previewType: FilePreviewType.TEXT,
    requiresConversion: false,
    maxFileSize: 10 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.SEARCH, PreviewFeature.TEXT_SELECT],
  },
  {
    fileType: "text/csv",
    previewType: FilePreviewType.SPREADSHEET,
    requiresConversion: true,
    conversionFormat: "html",
    maxFileSize: 25 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.SEARCH],
  },
  {
    fileType: "application/json",
    previewType: FilePreviewType.CODE,
    requiresConversion: false,
    maxFileSize: 5 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.SEARCH, PreviewFeature.TEXT_SELECT],
  },
  {
    fileType: "text/xml",
    previewType: FilePreviewType.CODE,
    requiresConversion: false,
    maxFileSize: 10 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.SEARCH, PreviewFeature.TEXT_SELECT],
  },
  {
    fileType: "text/html",
    previewType: FilePreviewType.TEXT,
    requiresConversion: false,
    maxFileSize: 10 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.SEARCH, PreviewFeature.TEXT_SELECT],
  },

  // Video Files
  {
    fileType: "video/mp4",
    previewType: FilePreviewType.VIDEO,
    requiresConversion: false,
    maxFileSize: 500 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.FULLSCREEN],
  },
  {
    fileType: "video/avi",
    previewType: FilePreviewType.VIDEO,
    requiresConversion: true,
    conversionFormat: "mp4",
    maxFileSize: 500 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.FULLSCREEN],
  },
  {
    fileType: "video/quicktime",
    previewType: FilePreviewType.VIDEO,
    requiresConversion: true,
    conversionFormat: "mp4",
    maxFileSize: 500 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.FULLSCREEN],
  },

  // Audio Files
  {
    fileType: "audio/mpeg",
    previewType: FilePreviewType.AUDIO,
    requiresConversion: false,
    maxFileSize: 100 * 1024 * 1024,
    supportedFeatures: [],
  },
  {
    fileType: "audio/wav",
    previewType: FilePreviewType.AUDIO,
    requiresConversion: false,
    maxFileSize: 100 * 1024 * 1024,
    supportedFeatures: [],
  },
  {
    fileType: "audio/ogg",
    previewType: FilePreviewType.AUDIO,
    requiresConversion: false,
    maxFileSize: 100 * 1024 * 1024,
    supportedFeatures: [],
  },

  // Archives (show contents)
  {
    fileType: "application/zip",
    previewType: FilePreviewType.ARCHIVE,
    requiresConversion: false,
    maxFileSize: 100 * 1024 * 1024,
    supportedFeatures: [],
  },
  {
    fileType: "application/x-rar-compressed",
    previewType: FilePreviewType.ARCHIVE,
    requiresConversion: false,
    maxFileSize: 100 * 1024 * 1024,
    supportedFeatures: [],
  },

  // CAD Files (for construction/engineering businesses)
  {
    fileType: "application/acad",
    previewType: FilePreviewType.CAD,
    requiresConversion: true,
    conversionFormat: "pdf",
    maxFileSize: 50 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.ZOOM, PreviewFeature.PAGINATION],
  },
  {
    fileType: "image/vnd.dwg",
    previewType: FilePreviewType.CAD,
    requiresConversion: true,
    conversionFormat: "pdf",
    maxFileSize: 50 * 1024 * 1024,
    supportedFeatures: [PreviewFeature.ZOOM],
  },
];
```

---

## 5. FILE INTEGRATION WITH ENTITIES

### 5.1 Entity File Attachments

**Customer Files Integration:**

```typescript
interface CustomerFileAttachment {
  customerId: string;
  fileId: string;
  attachmentType:
    | "contract"
    | "id_document"
    | "tax_document"
    | "correspondence"
    | "other";
  isPrimary: boolean;
  displayOrder: number;

  // Greek-Specific
  greekDocumentType?: GreekDocumentType;
  legalRequirement?: boolean;
  expirationDate?: Date;
}

enum GreekDocumentType {
  AFM_CERTIFICATE = "afm_certificate",
  BUSINESS_LICENSE = "business_license",
  TAX_CLEARANCE = "tax_clearance",
  CHAMBER_CERTIFICATE = "chamber_certificate",
  INSURANCE_CERTIFICATE = "insurance_certificate",
  BANK_DETAILS = "bank_details",
}
```

**Customer Detail - Files Tab:**

```
┌─ Customer: ACME Corp ──────────────────────────────────────────┐
│ [Details] [Files] [History] [Invoices] [Communication]        │
│ ──────────────────────────────────────────────────────────────── │
│ ┌─ Required Documents ─────────────────────────────────────────┐ │
│ │ ☑ AFM Certificate        [contract.pdf]        [View] [×]   │ │
│ │ ☑ Business License       [license.pdf]         [View] [×]   │ │
│ │ ☐ Tax Clearance          [Missing - Upload]    [Upload]     │ │
│ │ ☑ Chamber Certificate    [chamber.pdf]         [View] [×]   │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ ──────────────────────────────────────────────────────────────── │
│ ┌─ All Files ─────────────────────────────────────────────────┐ │
│ │ 📁 Contracts (3 files)                              [View] │ │
│ │ 📁 Invoices (15 files)                              [View] │ │
│ │ 📁 Correspondence (8 files)                         [View] │ │
│ │ 📁 Legal Documents (5 files)                        [View] │ │
│ │ 📁 Marketing Materials (2 files)                    [View] │ │
│ │                                                             │ │
│ │ Total: 33 files (125MB)                                    │ │
│ │ [+ Upload Files] [📁 File Manager] [🔍 Search Files]       │ │
│ └─────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

---

## 6. IMPLEMENTATION COMPONENTS

### 6.1 File Management Components

```typescript
// Core File Components
<FileManager
  entityType="customer"
  entityId={customerId}
  allowUpload={true}
  allowDelete={permissions.canDelete}
  showGreekCategories={true}
  enableAADECompliance={true}
/>

<FileUpload
  destination="customers"
  allowedTypes={['pdf', 'doc', 'jpg', 'png']}
  maxFileSize={100 * 1024 * 1024} // 100MB
  onUpload={handleFileUpload}
  greekDocumentRecognition={true}
/>

<FilePreview
  fileId={fileId}
  showComments={true}
  allowDownload={permissions.canDownload}
  showGreekMetadata={true}
/>

<FileList
  files={files}
  view="grid" // or "list"
  sortBy="name"
  filterBy={filters}
  enableSelection={true}
  enableDragAndDrop={true}
/>

// Greek-Specific Components
<GreekDocumentUpload
  documentType="afm_certificate"
  required={true}
  onUpload={handleGreekDocumentUpload}
/>

<AADEComplianceChecker
  fileId={fileId}
  onComplianceCheck={handleComplianceCheck}
/>
```

### 6.2 File Management Hooks

```typescript
// Core File Hooks
const useFileManager = (entityType: string, entityId: string) => {
  const [files, setFiles] = useState<FileRecord[]>([]);
  const [folders, setFolders] = useState<FileFolder[]>([]);
  const [loading, setLoading] = useState(false);

  const uploadFile = async (file: File, metadata: FileMetadata) => {
    // File upload logic
  };

  const deleteFile = async (fileId: string) => {
    // File deletion logic
  };

  const moveFile = async (fileId: string, destinationFolderId: string) => {
    // File move logic
  };

  return {
    files,
    folders,
    loading,
    uploadFile,
    deleteFile,
    moveFile,
  };
};

// Greek-Specific Hooks
const useGreekDocumentProcessor = () => {
  const processGreekDocument = async (file: File) => {
    // Greek document processing logic
  };

  const validateAADECompliance = async (fileId: string) => {
    // AADE compliance validation
  };

  return {
    processGreekDocument,
    validateAADECompliance,
  };
};
```

---

## 7. STORAGE QUOTAS & LIMITS

### 7.1 Storage Quota System

```typescript
interface StorageQuota {
  companyId: string;

  // Quota Limits
  maxStorageBytes: number;
  maxFilesCount: number;
  maxFileSizeBytes: number;

  // Current Usage
  currentStorageBytes: number;
  currentFilesCount: number;

  // Quota Policies
  quotaPolicy: "hard" | "soft" | "flexible";
  warningThreshold: number; // percentage

  // Subscription Integration
  subscriptionTier: string;
  overageAllowed: boolean;

  // Last Updated
  lastCalculated: Date;
  nextCalculation: Date;
}
```

### 7.2 Subscription-Based Storage

**Storage Tiers:**

- **Starter**: 1GB storage, 100 files, 10MB max file size
- **Professional**: 10GB storage, 1,000 files, 100MB max file size
- **Enterprise**: 100GB storage, 10,000 files, 1GB max file size
- **Custom**: Unlimited storage, unlimited files, custom file size limits

---

## 8. ADDITIONAL CONSIDERATIONS

### 8.1 Deployment-Specific Considerations

**SAAS Deployment:**

- **Multi-Tenancy**: Complete isolation between company files
- **Scalability**: Automatic scaling based on usage
- **Global Distribution**: CDN for fast access worldwide
- **Compliance**: SOC 2, ISO 27001, GDPR compliance
- **Backup**: Automated multi-region backups
- **Monitoring**: Real-time monitoring and alerting

**Local Installation:**

- **Data Sovereignty**: Files remain on customer premises
- **Backup Strategy**: Local backup with optional cloud sync
- **Security**: File-level encryption and access controls
- **Migration Path**: Easy migration to SAAS when needed
- **Compliance**: GDPR compliance with local data processing
- **Maintenance**: Automated maintenance and updates

### 8.2 File Migration Between Deployments

**SAAS to Local Migration:**

```typescript
interface MigrationTask {
  id: string;
  type: "saas_to_local" | "local_to_saas";
  companyId: string;
  status: "pending" | "in_progress" | "completed" | "failed";

  // Migration Details
  totalFiles: number;
  migratedFiles: number;
  failedFiles: number;
  estimatedTime: number;

  // Progress Tracking
  currentStep: string;
  progressPercentage: number;

  // Error Handling
  errors: MigrationError[];
  retryCount: number;

  // Verification
  checksumVerification: boolean;
  integrityCheck: boolean;
}
```

### 8.3 File Naming Conventions

**Automatic File Naming:**

```typescript
interface FileNamingStrategy {
  // Standard naming patterns
  invoicePattern: "{invoiceNumber}_{date}_{version}.pdf";
  contractPattern: "{customerName}_{contractType}_{year}.pdf";
  imagePattern: "{productId}_{imageType}_{timestamp}.{extension}";

  // Greek-specific naming
  greekDocumentPattern: "{documentType}_{afm}_{date}.pdf";
  aadeDocumentPattern: "AADE_{transactionId}_{date}.pdf";

  // Conflict resolution
  conflictResolution: "rename" | "version" | "replace";
  maxFilenameLength: 255;

  // Sanitization
  sanitizeGreekCharacters: boolean;
  allowUnicodeFilenames: boolean;
}
```

### 8.4 Performance Optimization

**SAAS Optimization:**

- **CDN Caching**: Aggressive caching for frequently accessed files
- **Lazy Loading**: Progressive loading for large file lists
- **Thumbnail Generation**: Automatic thumbnail creation
- **Compression**: Automatic file compression for storage efficiency
- **Prefetching**: Intelligent prefetching based on user behavior

**Local Optimization:**

- **Indexing**: File system indexing for fast search
- **Caching**: Local cache for frequently accessed files
- **Compression**: Optional file compression to save disk space
- **Cleanup**: Automatic cleanup of temporary files
- **Monitoring**: Disk usage monitoring and alerts

### 8.5 Disaster Recovery

**SAAS Disaster Recovery:**

- **Multi-Region Replication**: Automatic replication across regions
- **Point-in-Time Recovery**: Restore files to specific timestamps
- **Backup Verification**: Regular backup integrity checks
- **Recovery Testing**: Automated recovery testing
- **RTO/RPO**: Recovery Time Objective < 1 hour, Recovery Point Objective < 15 minutes

**Local Disaster Recovery:**

- **Local Backup**: Automated local backup schedules
- **External Backup**: Integration with external backup services
- **Backup Verification**: Checksum verification of backups
- **Recovery Procedures**: Documented recovery procedures
- **Testing**: Regular disaster recovery testing

### 8.6 Compliance & Auditing

**Audit Trail Requirements:**

```typescript
interface FileAuditLog {
  id: string;
  fileId: string;
  action: "upload" | "view" | "download" | "delete" | "share" | "modify";
  userId: string;
  timestamp: Date;

  // Context
  ipAddress: string;
  userAgent: string;
  sessionId: string;

  // Details
  oldValue?: any;
  newValue?: any;
  reason?: string;

  // Greek-specific
  aadeCompliance?: boolean;
  legalRequirement?: boolean;
}
```

**Compliance Features:**

- **GDPR Compliance**: Right to erasure, data portability, consent management
- **Greek Data Protection**: Local data processing requirements
- **Tax Compliance**: 7-year retention for tax documents
- **Legal Compliance**: Document retention policies
- **Industry Compliance**: Industry-specific compliance requirements

### 8.7 Integration Points

**CRM Integration:**

- Customer document attachments
- Automatic file categorization
- Customer communication history
- Contract management integration

**ERP Integration:**

- Invoice and receipt attachments
- Product documentation
- Financial document management
- Inventory documentation

**Greek Compliance Integration:**

- AADE document submission
- Tax document management
- Legal document workflows
- Compliance reporting

---

## 9. FILE PREVIEW AND MANAGEMENT APIS

### 9.1 File Preview APIs

**Get File Preview Information:**

```typescript
// Get file preview URL and capabilities
GET /api/files/{fileId}/preview
Response: {
  supported: boolean;
  previewUrl?: string;
  previewType: FilePreviewType;
  thumbnailUrl?: string;
  convertedFormats: ConvertedFormat[];
  supportedFeatures: PreviewFeature[];
  metadata: {
    fileName: string;
    fileType: string;
    size: number;
    dimensions?: { width: number; height: number };
    duration?: number;      // For video/audio files
    pageCount?: number;     // For documents
    exifData?: object;      // For images
  };
}

// Get file preview content (for inline viewing)
GET /api/files/{fileId}/preview-content
Query: {
  page?: number;          // For paginated content
  quality?: "low" | "medium" | "high";
  format?: "html" | "json" | "text";
}
Response: {
  content: string;        // HTML content for preview
  mimeType: string;       // Content type
  encoding: string;       // Content encoding
  pageCount?: number;     // Total pages
  currentPage?: number;   // Current page
}
```

**File Conversion APIs:**

```typescript
// Convert file to different format
POST /api/files/{fileId}/convert
Body: {
  targetFormat: string;   // "pdf", "html", "jpg", "png", "mp4", etc.
  quality?: number;       // 1-100 for image/video conversions
  pageRange?: string;     // "1-5" for document conversions
  options?: {
    resolution?: number;  // DPI for image conversions
    compression?: boolean; // Enable compression
    watermark?: string;   // Add watermark
  };
}
Response: {
  conversionId: string;
  status: "pending" | "processing" | "completed" | "failed";
  convertedUrl?: string;
  estimatedTime?: number; // Seconds
  expiresAt?: Date;       // When converted file expires
}

// Get conversion status
GET /api/files/conversions/{conversionId}
Response: {
  status: "pending" | "processing" | "completed" | "failed";
  progress?: number;      // 0-100 for processing
  convertedUrl?: string;
  originalFileId: string;
  targetFormat: string;
  error?: string;
  logs?: string[];
}

// Generate thumbnail
POST /api/files/{fileId}/thumbnail
Body: {
  size: "small" | "medium" | "large" | "custom";  // 150x150, 300x300, 600x600, custom
  dimensions?: { width: number; height: number };  // For custom size
  quality?: number;                                // 1-100
  crop?: "center" | "smart" | "top" | "bottom";   // Crop strategy
}
Response: {
  thumbnailUrl: string;
  size: number;
  dimensions: { width: number; height: number };
  cacheExpiry: Date;
}
```

### 9.2 File Management APIs

**Core File Operations:**

```typescript
// Upload file with preview processing
POST /api/files/upload
Body: FormData {
  file: File;
  folderId?: string;
  entityType?: string;    // "account", "invoice", "product"
  entityId?: string;
  category?: GreekDocumentCategory;
  tags?: string[];
  generatePreview?: boolean;
  generateThumbnail?: boolean;
}
Response: {
  fileId: string;
  fileName: string;
  fileSize: number;
  previewSupported: boolean;
  thumbnailGenerated: boolean;
  processingJobs: string[]; // IDs of background jobs
}

// Batch upload with preview
POST /api/files/batch-upload
Body: FormData {
  files: File[];
  folderId?: string;
  entityType?: string;
  entityId?: string;
  generatePreviews?: boolean;
}
Response: {
  uploads: FileUploadResult[];
  batchId: string;
  totalFiles: number;
  successCount: number;
  failedCount: number;
}

// Get file details with preview info
GET /api/files/{fileId}
Response: {
  id: string;
  fileName: string;
  fileType: string;
  size: number;
  previewSupported: boolean;
  previewType: FilePreviewType;
  previewUrl?: string;
  thumbnailUrl?: string;
  downloadUrl: string;
  createdAt: Date;
  modifiedAt: Date;
  metadata: FileMetadata;
  permissions: FilePermission[];
  greekCategory?: GreekDocumentCategory;
  aadeCompliant?: boolean;
}

// Update file metadata
PUT /api/files/{fileId}
Body: {
  fileName?: string;
  tags?: string[];
  category?: GreekDocumentCategory;
  description?: string;
  customFields?: Record<string, any>;
}
Response: {
  fileId: string;
  updated: boolean;
  reprocessPreview?: boolean; // If filename changed
}

// Delete file
DELETE /api/files/{fileId}
Response: {
  deleted: boolean;
  cleanupJobs: string[];  // Background cleanup jobs
}
```

### 9.3 Folder Management APIs

```typescript
// Create folder
POST /api/folders
Body: {
  name: string;
  parentId?: string;
  entityType?: string;
  entityId?: string;
  permissions?: FolderPermission[];
}
Response: {
  folderId: string;
  name: string;
  path: string;
  parentId?: string;
  createdAt: Date;
}

// Get folder contents with previews
GET /api/folders/{folderId}/contents
Query: {
  page?: number;
  limit?: number;
  sortBy?: "name" | "date" | "size" | "type";
  sortOrder?: "asc" | "desc";
  filter?: string;
  includePreviews?: boolean;
}
Response: {
  folders: FolderInfo[];
  files: FileInfo[];
  totalItems: number;
  currentPage: number;
  totalPages: number;
}

// Move file/folder
POST /api/files/{fileId}/move
Body: {
  targetFolderId: string;
  newName?: string;
}
Response: {
  moved: boolean;
  newPath: string;
  updatePreview?: boolean;
}
```

### 9.4 Search and Filter APIs

```typescript
// Advanced file search
GET /api/files/search
Query: {
  query?: string;         // Text search
  fileType?: string;      // MIME type or extension
  category?: GreekDocumentCategory;
  entityType?: string;
  entityId?: string;
  dateFrom?: Date;
  dateTo?: Date;
  sizeMin?: number;
  sizeMax?: number;
  hasPreview?: boolean;
  tags?: string[];
  page?: number;
  limit?: number;
}
Response: {
  files: FileSearchResult[];
  facets: {
    fileTypes: { type: string; count: number }[];
    categories: { category: string; count: number }[];
    tags: { tag: string; count: number }[];
  };
  totalResults: number;
  searchTime: number;
}

// Get file recommendations
GET /api/files/recommendations
Query: {
  entityType?: string;
  entityId?: string;
  fileType?: string;
  limit?: number;
}
Response: {
  recommendations: FileRecommendation[];
  reason: string;
}
```

### 9.5 Sharing and Collaboration APIs

```typescript
// Share file with preview
POST /api/files/{fileId}/share
Body: {
  shareType: "public" | "private" | "organization";
  permissions: ("view" | "download" | "comment")[];
  expiresAt?: Date;
  password?: string;
  allowPreview?: boolean;
  allowDownload?: boolean;
}
Response: {
  shareId: string;
  shareUrl: string;
  previewUrl?: string;
  permissions: string[];
  expiresAt?: Date;
}

// Get shared file info
GET /api/shares/{shareId}
Response: {
  fileId: string;
  fileName: string;
  fileType: string;
  size: number;
  previewSupported: boolean;
  previewUrl?: string;
  downloadUrl?: string;
  permissions: string[];
  expiresAt?: Date;
  requiresPassword: boolean;
}

// Add comment to file
POST /api/files/{fileId}/comments
Body: {
  text: string;
  position?: {           // For PDFs and images
    page?: number;
    x?: number;
    y?: number;
  };
  parentCommentId?: string;
}
Response: {
  commentId: string;
  text: string;
  userId: string;
  createdAt: Date;
  position?: any;
}
```

### 9.6 Greek-Specific APIs

```typescript
// Greek document validation
POST /api/files/{fileId}/validate-greek
Response: {
  isValid: boolean;
  documentType?: GreekDocumentCategory;
  extractedData?: {
    afm?: string;
    amka?: string;
    doy?: string;
    invoiceNumber?: string;
    amount?: number;
    date?: Date;
  };
  compliance: {
    aadeCompliant: boolean;
    taxCompliant: boolean;
    legalCompliant: boolean;
  };
  suggestions: string[];
}

// AADE document processing
POST /api/files/{fileId}/aade-process
Body: {
  documentType: "invoice" | "receipt" | "expense";
  autoSubmit?: boolean;
}
Response: {
  processedData: AADEDocumentData;
  validationResults: AADEValidationResult[];
  submissionId?: string;
  submissionStatus?: "pending" | "submitted" | "accepted" | "rejected";
}
```

---

## 10. CONCLUSION

This comprehensive file storage system provides:

**✅ Dual Deployment Support:**

- SAAS cloud storage with global CDN
- Local installation with filesystem storage
- Unified API for both deployment types
- Easy migration between deployments

**✅ Complete File Management:**

- Upload, organize, preview, share, and delete files
- Structured folder organization
- File versioning and backup
- Advanced search and filtering

**✅ Greek Business Integration:**

- Greek document recognition and categorization
- AADE compliance checking
- Greek tax document management
- Multi-language file descriptions

**✅ Enterprise-Grade Features:**

- Encrypted file storage
- Access control and permissions
- Comprehensive audit trails
- Disaster recovery capabilities

**✅ Performance & Scalability:**

- Optimized for both deployment types
- Automatic scaling and caching
- Performance monitoring and optimization
- Efficient storage utilization

This file storage system enhances the Greek ERP/CRM platform by providing enterprise-grade document management while maintaining the Greek business focus and compliance requirements, with full support for both SAAS and local deployment models.
