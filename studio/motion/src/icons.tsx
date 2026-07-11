// icons.tsx — the ONE icon surface for the motion studio.
//
// Brand-neutral: re-exports lucide-react glyphs so no ported file ever imports a
// product-specific icon pack. Import icons from here (`@ui`-adjacent) rather than
// reaching into lucide-react directly, so the set stays curated and swappable.
//
// lucide icons take {size, color, strokeWidth} props — matching the shape the UI
// kit's CleanButton/FormInput expect for an `icon` prop.
export {
  Zap,
  Check,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  ChevronLeft,
  X,
  Plus,
  Search,
  Settings,
  User,
  Users,
  Mail,
  Phone,
  Calendar,
  Clock,
  FileText,
  Bell,
  ArrowRight,
  ArrowUpRight,
  Sparkles,
  Send,
  Trash2,
  Pencil,
  Play,
  Pause,
} from "lucide-react";
